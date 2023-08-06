
from allensdk.api.queries.rma_api import RmaApi

import pandas as pd
import numpy as np
import glob

import pkg_resources

from . import Utils
import copy 

Z_SCORE = 'z-score'
EXPR_LVL = 'expression_level'
REGION_ASSIGNMENT = 'mapped region'

VALUE_COLUMNS = [EXPR_LVL,Z_SCORE] 

DATAFRAME_CACHE = "cache\\data-frames\\"

Genes = ["Gabra1", "Gabra2", "Gabra4", "Gabra5", "Gabrb1", "Gabrb2", "Gabrb3", "Gabrd", "Gabrg2", "Gabrg3"]

# ! here, some magic happens. these lists define - amongst the available options in dropdowns, their labels, and defaults - also some interactions with the charts.
# ! the type defines the named parameter that is provided to the chart-functions. 
GENE_LIST = Utils.DropDownListConfiguration(label='Gene', type='gene', 
  data=Genes,
  default='Gabra4', defaultLeft='Gabra4', defaultRight='Gabrb3')

# for co-expressions, we need additional gene-selection. this ensure that the type is correctly bound to the expected parameters
GENE1_LIST = Utils.DropDownListConfiguration(label='Gene', type='gene1', 
  data=Genes,
  default='Gabra4', defaultLeft='Gabra4', defaultRight='Gabra4')

GENE2_LIST = Utils.DropDownListConfiguration(label='vs', type='gene2', 
  data=Genes,
  default='Gabra4', defaultLeft='Gabra5', defaultRight='Gabra5')

AGGREGATION_FUNCTIONS = Utils.DropDownListConfiguration(label='Aggregation function', type='aggregation_function', 
  data=['min', 'max', 'mean', 'var'], 
  default='mean', defaultLeft='mean',defaultRight='var')

SPECIES = Utils.DropDownListConfiguration(label=None, type='species', 
  data=['human', 'mouse - sagittal', 'mouse - coronal'], 
  default='human', defaultLeft= 'human', defaultRight= 'mouse - sagittal')

STRUCTURE_LEVELS = Utils.DropDownListConfiguration(label='Level', type='structure_level', 
  data=[l for l in range(0,10)], 
  default=2, defaultLeft= 2, defaultRight= 2)

# this is used to define how to aggregate already aggregated values. e.g., aggregating the (expression-level, max)-column uses np.max.
AGGREGATION_AGGREGATES = { 'min': np.min, 'max': np.max, 'mean': np.mean, 'var': np.mean }

class AllenSdkHelper:
  def __init__(self):
    self.rma = RmaApi() 
    
    # TODO: only load this, if the file does not exist!
    self.PlaneOfSections = self.rma.json_msg_query(
            url="http://api.brain-map.org/api/v2/data/query.json?criteria=model::PlaneOfSection,rma::options[num_rows$eqall]"
        )

    # path=Utils.makedir(f'cache\\models') + '\\PlaneOfSection.json',

  def getPlaneOfSections(self):
    return self.PlaneOfSections

allenSdkHelper = AllenSdkHelper()

PlaneOfSections = {x['id']: x['name'] for x in allenSdkHelper.getPlaneOfSections()} 

__opposing = { 'Human': 'Mouse', 'Mouse': 'Human' }

userRegionAssignmentsPath = "region-assignments.csv"
if glob.glob(userRegionAssignmentsPath):
  print(f'Using file {userRegionAssignmentsPath} found in your working-directory.')
  __regionAssignmentsRaw = pd.read_csv(userRegionAssignmentsPath, header=0)
else:  
  # no file provided by the user. read it from the pkg_resources
  print(f'No file {userRegionAssignmentsPath} found in your working-directory. Defaulting to shipped assignments.')
  regionAssignmentsPath = ".\\annotations\\region-assignments.csv"
  # from https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
  resource_package = 'geneEcomparison'
  resource_path = '/'.join(('annotations', 'region-assignments.csv'))  # Do not use os.path.join()
  shippedAssignmentsStream = pkg_resources.resource_stream(resource_package, resource_path)
  __regionAssignmentsRaw = pd.read_csv(shippedAssignmentsStream, header=0)
  

__regionAssignments = { species: __regionAssignmentsRaw.apply(lambda x: 
    { (x[species].split(';')[0], x[species].split(';')[1]) :
     { 'assignment': (x[__opposing[species]].split(';')[0], x[__opposing[species]].split(';')[1]) ,
     'name': x['Name'] }
    } ,axis=1)
     for species in ['Human', 'Mouse'] }

# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_dict.html
RegionAssignments = Utils.simple( { 
  'asList': __regionAssignments,
  'asDict': { 
    'Human': Utils.combine_dicts(__regionAssignments['Human'].to_list()),
    'Mouse': Utils.combine_dicts(__regionAssignments['Mouse'].to_list()) }
})
