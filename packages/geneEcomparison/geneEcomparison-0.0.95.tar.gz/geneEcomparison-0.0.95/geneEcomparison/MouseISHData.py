
from allensdk.api.queries.rma_api import RmaApi
from allensdk.api.queries.grid_data_api  import GridDataApi

from allensdk.api.queries.reference_space_api import ReferenceSpaceApi
from allensdk.core.reference_space import ReferenceSpace

import numpy as np
import pandas as pd
import glob

import concurrent
import concurrent.futures

from . import Utils
from . import Constants
from . import StructureMap

class MouseISHData:
  VALUE_COLUMNS = [Constants.EXPR_LVL, Constants.Z_SCORE] 

  currentGets = {}

  def __init__(self, geneAcronym):
    self.geneAcronym = geneAcronym
    self.cache_path = Constants.DATAFRAME_CACHE + f'mouse\\{geneAcronym}\\'

  def get(self, from_cache, aggregations):
  
    if from_cache:
      return self.getAsync(from_cache, aggregations)

    if self.geneAcronym in MouseISHData.currentGets:
      print(f'Waiting for initial request of mouse gene {self.geneAcronym} to complete...')
      done, not_done = concurrent.futures.wait([MouseISHData.currentGets[self.geneAcronym]], 
       return_when=concurrent.futures.FIRST_COMPLETED) # this wants an array... ok
      
      for fut in done:
        print(fut, 'exception:', fut.exception())
        return fut.result() 

    else: 
      with concurrent.futures.ThreadPoolExecutor() as executor:
        MouseISHData.currentGets[self.geneAcronym] = executor.submit(self.getAsync, from_cache, aggregations)
        return MouseISHData.currentGets[self.geneAcronym].result()

  def getAsync(self, from_cache, aggregations): 
    # load data once with from_cache = False, then change it to True to read it from disk instead of fetching it from the api
    if not from_cache:
      # we use the RmaApi to query specific information, such as the section data sets of a specific gene
      # for docs, see: https://alleninstitute.github.io/AllenSDK/allensdk.api.queries.rma_api.html
      rma = RmaApi() 
      
      # there might be a way to retrieve data in higher resolution, as stated here (default is 25, 10 is also available - but resolution is ignored for download_gene_expression_grid_data)
      # https://alleninstitute.github.io/AllenSDK/_modules/allensdk/api/queries/grid_data_api.html
      # See `Downloading 3-D Projection Grid Data <http://help.brain-map.org/display/api/Downloading+3-D+Expression+Grid+Data#name="Downloading3-DExpressionGridData-DOWNLOADING3DPROJECTIONGRIDDATA">`_
      gdApi = GridDataApi()

      # http://api.brain-map.org/examples/rma_builder/index.html
      # http://api.brain-map.org/examples/rma_builder/rma_builder.html
      # https://allensdk.readthedocs.io/en/latest/data_api_client.html
      sectionDataSets = pd.DataFrame( 
          rma.model_query(                
                model='SectionDataSet',
                #! criteria="plane_of_section[name$eqcoronal]", note that saggital only spans the left hemisphere, so this is tough to compare with human data.
                filters={'failed':'false'},
                include=f"genes[acronym$il{self.geneAcronym}],products[id$eq1]", # $il = case-insensitive like | yes, weird notation... id = 1 = mouse brain atlas (not developing!)
                num_rows='all')
      )
       
      # model's documentation: http://api.brain-map.org/doc/SectionDataSet.html
      # https://community.brain-map.org/t/attempting-to-download-substructures-for-coronal-p56-mouse-atlas/174/2

      experiments = {}
      
      # http://help.brain-map.org/display/mousebrain/Documentation
      annotations = np.fromfile(Utils.getRelativeFilepath("annotations\\P56_Mouse_gridAnnotation\\gridAnnotation.raw"), dtype="uint32")

      # https://community.brain-map.org/t/how-to-acquire-the-structure-label-for-the-expression-grid-data/150/4
      # for Mouse P56, structure_graph_id = 1 according to http://help.brain-map.org/display/api/Atlas+Drawings+and+Ontologies
      structure_map = StructureMap.StructureMap(reference_space_key = 'annotation/ccf_2017', resolution=25).get(structure_graph_id=1) # , annotation, meta 
      # from http://alleninstitute.github.io/AllenSDK/_static/examples/nb/reference_space.html#Downloading-an-annotation-volume

      for index, row in sectionDataSets.iterrows(): # https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
          exp_id = row['id']
          exp_path = f"cache\\mouse_ish-expr\\{exp_id}\\"
          
          try:
              # https://community.brain-map.org/t/whole-mouse-brain-gene-expression-data/447/4
              # explanation of what "energy" means here:
              # expression density = sum of expressing pixels / sum of all pixels in division
              # expression intensity = sum of expressing pixel intensity / sum of expressing pixels
              # expression energy = expression intensity * expression density

              gdApi.download_gene_expression_grid_data(exp_id, GridDataApi.ENERGY, exp_path)

              expression_levels = np.fromfile(exp_path + "energy.raw",  dtype=np.float32)

              # According to the doc @ http://help.brain-map.org/display/api/Downloading+3-D+Expression+Grid+Data
              # we have "A raw uncompressed float (32-bit) little-endian volume representing average expression energy per voxel. 
              # A value of "-1" represents no data. This file is returned by default if the volumes parameter is null."
              data = pd.DataFrame({Constants.EXPR_LVL: expression_levels, "structure_id": annotations})

              # some expression_levels are assigned to a structure of id 0. same is true for Jure's approach.
              # according to the Allen institue, this is just due to background-noise: 
              # https://community.brain-map.org/t/how-to-acquire-the-structure-label-for-the-expression-grid-data/150/4
              # values of -1 mean "no value obtained", hence we filter them out:
              data = data[(data[Constants.EXPR_LVL] != -1) & (data.structure_id != 0)]

              data[Constants.Z_SCORE] = Utils.z_score(data[Constants.EXPR_LVL])

              # https://stackoverflow.com/questions/31528819/using-merge-on-a-column-and-index-in-pandas
              # https://stackoverflow.com/questions/45147100/pandas-drop-columns-with-all-nans                

              name = f'mouse_{exp_id}_{Constants.PlaneOfSections[row["plane_of_section_id"]]}'
              data = Utils.merge_with_structure(data, structure_map, MouseISHData.VALUE_COLUMNS, aggregations)

              Utils.save(data, self.cache_path, name + '.pkl')

              experiments['mouse - ' + Constants.PlaneOfSections[row["plane_of_section_id"]]] = data
          except Exception as e:
              print(f"Error retrieving mouse-ish experiment {exp_id}: {str(e)}")
              raise e

      return experiments
    else:
      if not glob.glob(self.cache_path):
        Utils.log.warning(f"No cached dataframe found. Check whether you have access to file '{self.cache_path}' and whether it exists. Obtaining data without caching now...")
        return self.get(False, aggregations)
      
      return { 'mouse - ' + Utils.getFilename(file).split('_')[2]: Utils.load(file) for file in glob.glob(f'{self.cache_path}/*.pkl') }          
