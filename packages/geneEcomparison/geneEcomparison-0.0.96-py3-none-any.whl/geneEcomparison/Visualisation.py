
# used for data-visualisation
import plotly.graph_objects as go
import plotly.express as px

# library for providing an interactive web-interface (react-based)
import dash
from dash import Dash, no_update
import dash_bootstrap_components as dbc # used for css
import dash_core_components as dcc 
import dash_html_components as html # basic html-components
from dash.dependencies import Input, Output, State, MATCH, ALL # used for callback-functions
from dash_extensions import Download # provide general download-capabilities
from dash_extensions.snippets import send_data_frame # helps us provide downloadable data-frames

import dash_table # the component for showing data in a grid. also see: https://community.plotly.com/t/loading-pandas-dataframe-into-data-table-through-a-callback/19354/14

import webbrowser
from threading import Timer
import traceback # used for printing the stacktrace of callback-exceptions

from .HumanMicroarrayData import HumanMicroarrayData
from .MouseISHData import MouseISHData

from . import Comparison
from .Constants import AGGREGATION_AGGREGATES, AGGREGATION_FUNCTIONS, SPECIES, STRUCTURE_LEVELS, Z_SCORE
from . import Constants
from . import Utils

import sys
import json


# we use some icons from the font-awesome library:
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"

# ! adjust lists declared in Constants.py (such as GENE_LIST) to change the dropdown-list's options.

# ? For some good tutorials on Dash (https://dash.plotly.com/), see:
# ? https://www.youtube.com/watch?v=Ldp3RmUxtOQ
# ? https://www.youtube.com/watch?v=hSPmj7mK6ng

class WebInterface:
  def __init__(self, name, port = 5000):

    # for layout & css, see https://dash.plotly.com/layout
    self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX, FONT_AWESOME])
    self.port = port
   
    self.app.title = "Gene-expression comparison"
    self.header = [html.Span('Z-scores', id="z_score", style={"textDecoration": "underline", "cursor": "pointer"}), 
      # we need to use unicode, because html cannot be rendered without circumventing react's html-sanitizer (which is a security-feature)
      # formatting with line-breaks: https://community.plotly.com/t/dash-bootstrap-components-tooltip-multiple-lines/42285/2
      dbc.Tooltip(dcc.Markdown("= (\u0078 - \u03bc) / \u03C3\n\nMeasures how many standard-deviations the given value is afar from the population's mean."), target="z_score", style={"font-size": "16px"}), 
      ' of gene-expression by species & region']
    self.credits ="by Christoph Hüsson & Jure Fabjan"
    self.description = [
      "All data obtained from Allen Brain Institute: Human microarray-data vs rodent in-situ hybridization. Note that 'mouse - sagittal' only provides data for left hemisphere. However, for some genes, coronal data is not available for mice.",
      html.Br(), 
      "Double-click on a legend-entry to isolate associated data-points, e.g. to only view co-expressions of a specific region."]
    self.downloads = {}

    self.loadingColor = "#88888888"
    VIEWS = Utils.simple({
      'coexpressions': Utils.simple({ 'name': 'coexpressions', 'fn': self.coexpressions}), 
      'stackedBarsBySpecies': Utils.simple({'name': 'stackedBarsBySpecies', 'fn': self.stackedBarsBySpecies}),
      'allSpecies': Utils.simple({ 'name': 'allSpecies', 'fn': self.heatmapByRegion}),
      'gridView': Utils.simple({ 'name': 'gridView', 'fn': self.getTableData})
    })

    # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
    self.app.layout = html.Div([
        html.H1(self.header, className="pl-4 pt-2"),
        html.Span(self.credits, className="pl-4 text-muted", style={ 'position': 'absolute', 'top': '0.5rem', 'right': '0.5rem'}),
        html.P(self.description, className="pl-4"),
        dbc.Row(dbc.InputGroup([
          dbc.InputGroupAddon(
            dbc.Button("Add gene", id="gene_input_button", n_clicks=0),
            addon_type="prepend"),
          dbc.Input(id="gene_input", placeholder="New gene", type="text")
          ])),
        # TODO: explain z-score with a tooltip: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/tooltip/ 
        dbc.Tabs([
          dbc.Tab(self.sideBySideView(VIEWS.allSpecies.name, [AGGREGATION_FUNCTIONS], [Constants.GENE_LIST]),  
            label="Expression-heatmaps"),
          dbc.Tab(self.sideBySideView(VIEWS.coexpressions.name, [AGGREGATION_FUNCTIONS], [SPECIES, Constants.GENE1_LIST, Constants.GENE2_LIST, STRUCTURE_LEVELS]),
           label="Co-expressions"),
          dbc.Tab(self.sideBySideView(VIEWS.stackedBarsBySpecies.name, [AGGREGATION_FUNCTIONS], [SPECIES, Constants.GENE_LIST, STRUCTURE_LEVELS]), 
           label="Stacked bars"),
          dbc.Tab(self.gridView(VIEWS.gridView.name, [SPECIES, Constants.GENE_LIST, STRUCTURE_LEVELS]), label="Data-grid")
        ]),
    ])

    # Adding a single gene into the dropdown menus
    @self.app.callback(
    Output({'type': "gene", "input": True, "view": ALL}, "options"),
    Output({'type': "gene", "input": True, "view": ALL, "side": ALL}, "options"),
    Output({"type": "gene1", "input": True, "view": ALL, "side": ALL}, "options"),
    Output({"type": "gene2", "input": True, "view": ALL, "side": ALL}, "options"),
    Output("gene_input", "value"),
    [Input("gene_input_button", "n_clicks")],
    [State("gene_input", "value"),
    State({'type': "gene", "input": True, "view": ALL}, "options"),
    State({'type': "gene", "input": True, "view": ALL, "side": ALL}, "options"),
    State({"type": "gene1", "input": True, "view": ALL, "side": ALL}, "options"),
    State({"type": "gene2", "input": True, "view": ALL, "side": ALL}, "options"),])
    def geneListUpdate(n_clicks, gene_name, list1, list2, list3, list4):
      if n_clicks:
        Constants.Genes.append(gene_name)
        output_list = [{ "label": i, "value": i } for i in Constants.Genes]
        return [output_list for _ in list1], [output_list for _ in list2], [output_list for _ in list3], [output_list for _ in list4], ""
      else:
        raise dash.exceptions.PreventUpdate

    @self.app.server.route('/shutdown', methods=['GET'])
    def shutdown():
      sys.exit();
      return 'Server shutting down...'

    # from: https://community.plotly.com/t/allowing-users-to-download-csv-on-click/5550/42
    @self.app.callback(Output({'type': 'download', 'view': MATCH}, "data"), Input({'type': 'download-button', 'view': MATCH}, "n_clicks"))
    def downloadCallback(n_clicks):
      if not n_clicks is None:
        dl = self.downloads['grid']

        return send_data_frame(dl['data'].to_excel, dl['filename'] + '.xlsx', index=True)
      else:
        return no_update

    # we need to update left/right side https://dash.plotly.com/pattern-matching-callbacks
    # see https://dash-bootstrap-components.opensource.faculty.ai/docs/components/input/
    @self.app.callback( 
      # MATCH is a bit tricky. in this case, it basically says that all inputs and outputs need to belong to the same view
      # for a doc on available output-properties (figure, hidden, etc.), check out: https://dash.plotly.com/dash-html-components/output
      [Output({'type': 'graph', 'side': 'left', 'view': MATCH}, "figure"), 
      # graphs do NOT have a 'hidden'-property. setting their style in the callback would override previously set style-settings, such as the graph's dimensions.
      # instead, we use a wrapper-div, which provides us with a hidden property.
       Output({'type': 'graph-container', 'side': 'left', 'view': MATCH}, "hidden"), 
       Output({'type': 'graph', 'side': 'right', 'view': MATCH}, "figure"),
       Output({'type': 'graph-container', 'side': 'right', 'view': MATCH}, "hidden"),
       Output({'type': 'alert', 'side': 'left', 'view': MATCH}, "children"),
       Output({'type': 'alert', 'side': 'left', 'view': MATCH}, "is_open"),
       Output({'type': 'alert', 'side': 'right', 'view': MATCH}, "children"),
       Output({'type': 'alert', 'side': 'right', 'view': MATCH}, "is_open")], 
       # we need to separate the side-specific graphs from the inputs. we use input: True to filter out non-input-controls
      [Input({'type': ALL, 'input': True, 'view': MATCH}, "value"), 
       Input({'type': ALL, 'input': True, 'side': 'left', 'view': MATCH}, "value"), 
       Input({'type': ALL, 'input': True, 'side': 'right', 'view': MATCH}, "value")])
    def sideBySideViewCallback(common, left, right): # these parameters are actually not required / usable, because the real inputs are provided dynamically
      
      # we don't want to update a side if only the opposing side's gene has been changed
      # https://dash.plotly.com/advanced-callbacks
      ctx = dash.callback_context

      # https://stackoverflow.com/questions/4547274/convert-a-python-dict-to-a-string-and-back
      # the prop_id is a stringified dictionary (ugh...) so we need to json.loads it. but it is provided in the format 'stringified_dict.value', so we split it...
      # ! we cant use eval here, because Dash lowercases the property-values, which changes True to true. eval does not recognize this as a keyword and crashes
      input_props = json.loads(ctx.triggered[0]['prop_id'].split('.')[0]) if ctx.triggered else {}

      common = self.callbackInputsToKwags(ctx.inputs_list[0])
      left = self.callbackInputsToKwags(ctx.inputs_list[1])
      right = self.callbackInputsToKwags(ctx.inputs_list[2])

      # handle the initial load, which is provided with triggered = False. changing non-side related inputs, however, forces a reload of both sides
      if not ctx.triggered or 'side' not in input_props: 
        left_unchanged = False
        right_unchanged = False
      else:
        # check which input triggered this callback. there can only be one input at a time, so we only check the first element:
        left_unchanged = (input_props['side'] != "left")
        right_unchanged = (input_props['side'] != "right")

      # the function used for creating the chart-figure is defined as a pointer in the views-object:
      fn = getattr(VIEWS, ctx.outputs_list[0]['id']['view']).fn

      retLeft = None
      retRight = None 

      errLeft = None
      errRight = None

      if not left_unchanged:
        try:
          retLeft = fn(**common, **left, side='left')
        except Exception as e:
          # https://stackoverflow.com/questions/4308182/getting-the-exception-value-in-python
          traceback.print_exc()
          errLeft = str(e)

      if not right_unchanged:
        try:
          retRight = fn(**common, **right, side='right')
        except Exception as e:
          traceback.print_exc()
          errRight = str(e)

      # https://community.plotly.com/t/i-want-to-create-a-conditional-callback-in-dash-is-it-possible/23418/2
      # we are able to prevent an update of one side. however, the loading-indicator will still be shown. 
      # track this bug here: https://github.com/plotly/dash/issues/1120

      return (
        {} if errLeft else no_update if left_unchanged else retLeft, 
        not not errLeft,
        {} if errRight else no_update if right_unchanged else retRight,
        not not errRight,
        no_update if errLeft is None else errLeft, # alert-text
        not (errLeft is None), # alert is_open
        no_update if errRight is None else errRight,
        not (errRight is None)
        )

        
    @self.app.callback( 
      # MATCH is a bit tricky. in this case, it basically says that all inputs and outputs need to belong to the same view
      Output({'type': 'grid', 'view': MATCH}, "children"), 
        # we need to separate the side-specific graphs from the inputs. we use input: True to filter out non-input-controls
      Input({'type': ALL, 'input': True, 'view': MATCH}, "value"))
    def gridViewCallback(common): # these parameters are actually not required / usable, because the real inputs are provided dynamically
      
      # we don't want to update a side if only the opposing side's gene has been changed
      # https://dash.plotly.com/advanced-callbacks
      ctx = dash.callback_context

      common = self.callbackInputsToKwags(ctx.inputs_list[0])

      # the function used for creating the chart-figure is defined as a pointer in the views-object:
      fn = getattr(VIEWS, ctx.outputs_list['id']['view']).fn

      data = Utils.unstack_columns(fn(**common))
      
      # dash_pivottable.PivotTable looks nice, but doesnt work in our scenario very well...
      # https://dash.plotly.com/datatable
      return dash_table.DataTable(
           data=data.to_dict('records'),
          columns=[{"name": i, "id": i} for i in data.columns],
          fixed_rows={ 'headers': True, 'data': 0 },
          filter_action="native",
          sort_action="native",
          sort_mode="multi",
          style_cell={'textAlign': 'left'},
          style_cell_conditional=[
              {
                  'if': {'column_id': c},
                  'textAlign': 'right'
              } for c in data.columns if 'z-score' in c
          ],
          # virtualization=True, cant use it: https://community.plotly.com/t/dash-data-table-with-virtualization-seems-to-break-completely-when-hidden-on-startup/29328
          # make the datatable acquire all space of its container: https://community.plotly.com/t/dynamic-dash-datatable-height/44061
          # also see: assets/styles.css
          style_table={"height": "calc(100vh - 272px)",
           "width": "calc(100vw - 40px)",
           "overflow": "auto",
           "display": "flex",
           "flex-flow": "column"}, #{'overflow-x': 'auto'}, #calc(100vh - 120px)
          style_data_conditional=[
          {
              'if': {'row_index': 'odd'},
              'backgroundColor': 'rgb(248, 248, 248)'
          }
          ]
        )
      
  def heatmapByRegion(self, aggregation_function, gene, side):
    
    return heatmap(Comparison.byDonor(
      HumanMicroarrayData(gene).get(from_cache=True, aggregations=AGGREGATION_FUNCTIONS.data),
      MouseISHData(gene).get(from_cache=True, aggregations=AGGREGATION_FUNCTIONS.data),
      aggregation_function
    ))

  # TODO: enforce same scaling for both sides to make the visual data comparable
  def coexpressions(self, aggregation_function, structure_level, species, gene1, gene2, side):
    structure_level = f"level_{structure_level}"
    sizeBy = f"shared_{aggregation_function}"

    if(gene1 == gene2):
      raise Exception("Co-expressions for the same gene of the same species make no sense.")

    result1 = Comparison.species_map[species](gene1).get(from_cache=True, aggregations=AGGREGATION_FUNCTIONS.data)[species]

    result2 = Comparison.species_map[species](gene2).get(from_cache=True, aggregations=AGGREGATION_FUNCTIONS.data)[species]

    # sometimes, there is no coronal or sagittal data
        
    data = Comparison.coexpression(result1, result2, aggregation_function, structure_level, gene1, gene2) 

    # https://plotly.com/python-api-reference/generated/plotly.express.scatter
    fig = px.scatter(Utils.sort_case_insensitive(data, structure_level), 
          y=f"{Z_SCORE}_{gene1}_{aggregation_function}", 
          x=f"{Z_SCORE}_{gene2}_{aggregation_function}"
          # TODO: there is some issue with sizes. besides NaN, we got some weird errors...
	        #,size=sizeBy#, size_max=400 
          ,color=structure_level
          ,opacity=0.65
          # https://plotly.com/javascript/reference/#parcats-dimensions-items-dimension-categoryorder
          #,dimensions={'categoryorder':'category ascending'} # sort categories 
          )

    
    fig.update_yaxes(title=gene1)
    fig.update_xaxes(title=gene2)           

    return fig

  def stackedBarsBySpecies(self, aggregation_function, structure_level, species, gene, side):
    result = Comparison.species_map[species](gene).get(from_cache=True, aggregations=AGGREGATION_FUNCTIONS.data)[species]

    return heatmap(Comparison.by_region(
      result.structure, 
      aggregation_function, Z_SCORE, f'level_{structure_level}', 'structure_name')
    )

  def callbackInputsToKwags(self, input):
    return { input[i]['id']['type']:input[i]['value']  for i in range(0,len(input)) }

  def gridView(self, viewName, filters):
    return html.Div([
          dbc.Card(dbc.CardBody(
            dbc.Form( # we get an array (label + dropdown) inside an array. so we need to unpack that
              dbc.FormGroup(Utils.unpack(self.dropDownByList(lst, {'type': lst.type, 'view': viewName}, value=lst.default) for lst in filters)
              + self.downloadButton(id={'type': 'download-button', 'view': viewName},viewName=viewName))
            , inline=True), className="p-2")), 
            dbc.Row(
                dbc.Col(
            dcc.Loading(html.Div(id={ 'type': 'grid', 'view': viewName }, children=[], className="mt-3"
             ), color=self.loadingColor)
          ))], className="p-2", style={ 'width': 'calc(100vw - 24px)'}) 

  def getTableData(self, species, gene, structure_level):

    result = Comparison.species_map[species](gene).get(from_cache=True, aggregations=AGGREGATION_FUNCTIONS.data)[species]

    value_columns = [(Z_SCORE, agg) for agg in AGGREGATION_FUNCTIONS.data]
    agg_dict = { (Z_SCORE, agg): AGGREGATION_AGGREGATES[agg] for agg in AGGREGATION_FUNCTIONS.data }
    
    # structure_level is provided as a string, because it stems from a dropdown-callback... we need to cast it to int
    result = result.structure.groupby([f'level_{i}' for i in range(0, int(structure_level) + 1)], dropna=True)[value_columns].agg(agg_dict).dropna()
    
    result = Utils.drop_columns_if(result.reset_index(), ['INDEX'])
    
    self.downloads['grid'] = { 'filename': f"{species}_{gene}_{structure_level}", 'data': result }
    return result
  
  # TODO: two range-sliders (for x and y) on common-control-div to allow synchronization of axis. 
  # # TODO or maybe is it possible to callback to hidden controls to then trigger updates on the axis?
  def sideBySideView(self, viewName, commonFilters, sideFilters):
    dimensions = Utils.simple({ 'w': 'calc(49vw - 30px)', 'h': 'calc(100vh - 340px)' })

    return html.Div([
          dbc.Card(dbc.CardBody(
          dbc.Form( # we get an array (label + dropdown) inside an array. so we need to unpack that
            dbc.FormGroup(Utils.unpack(self.dropDownByList(lst, {'type': lst.type, 'view': viewName}, value=lst.default) for lst in commonFilters))
          , inline=True), className="p-2")),
          dbc.Row([
                dbc.Col([ # start of left col
                  dbc.Row(
                    dbc.Form(
                      dbc.FormGroup( # TODO: make this responsive, because they overlap on smaller screens
                        Utils.unpack(self.dropDownByList(lst, {'type': lst.type, 'side': 'left', 'view': viewName}, value=lst.defaultLeft) for lst in sideFilters)
                      ), inline=True, className="ml-4 mt-3")
                  ),
                  dcc.Loading([ # TODO: move loading-panel to also encapsulate alerts. then, they will disappear on change of parameters
                    dbc.Row(
                      dbc.Alert(children="", 
                      id={ 'type': 'alert', 'view': viewName, 'side': 'left'},
                      is_open=False, color="danger", className="ml-3 mr-2 mt-1 w-100"),
                    ),
                    dbc.Row(
                      html.Div(
                        dcc.Graph(id={ 'type': 'graph', 'view': viewName, 'side': 'left'}, config={'scrollZoom': True}, style={'width': dimensions.w, 'height': dimensions.h})
                      ,id={ 'type': 'graph-container', 'view': viewName, 'side': 'left'}), className="ml-2 mt-3")
                  ],color=self.loadingColor, className="w-100 h-100")
                ], className="border-right"), # end of left col
                dbc.Col([ # start of right col
                  dbc.Row(
                    dbc.Form(
                      dbc.FormGroup(
                        Utils.unpack(self.dropDownByList(lst, {'type': lst.type, 'side': 'right', 'view': viewName}, value=lst.defaultRight) for lst in sideFilters)
                      ), inline=True, className="ml-4 mt-3")
                  ),
                  dcc.Loading([
                  dbc.Row(
                    dbc.Alert(children="", 
                    id={ 'type': 'alert', 'view': viewName, 'side': 'right'},
                    is_open=False, color="danger", className="ml-2 mr-3 mt-1 w-100"),
                  ),
                  dbc.Row(html.Div(
                    dcc.Graph(id={ 'type': 'graph', 'view': viewName, 'side': 'right'}, config={'scrollZoom': True}, style={'width': dimensions.w, 'height': dimensions.h})
                 ,id={ 'type': 'graph-container', 'view': viewName, 'side': 'right'}), className="ml-2 mt-3")
                ] ,color=self.loadingColor)
                ]) # end of right col
          ])
        ], className="p-2", style={ 'width': 'calc(100vw - 8px)'})

  # https://community.plotly.com/t/gluphicons-in-bootstrap-buttons/23438/2
  def downloadButton(self, viewName, **kwags):
    return [dbc.Button([html.I(className="fas fa-download fa-lg")], **kwags), dcc.Loading(Download(id={'type': 'download', 'view': viewName}), color=self.loadingColor)]

  def dropDownByList(self, lst, idProps, **kwags):
    return ([dbc.Label(lst.label, className="mr-2")] if not lst.label is None else []) + [dbc.Select(id={'type': lst.type, 'input': True, **idProps}, 
      options=[{ "label": g, "value": g } for g in lst.data], className="mr-3", **kwags)]

  def run_server(self, **kwags):
    return self.app.run_server(**kwags, port=self.port)

  def __open(self):
    webbrowser.open_new("http://localhost:{}".format(self.port))

  def open_browser(self):
    Timer(1, self.__open).start()
    
# https://stackoverflow.com/questions/36898008/seaborn-heatmap-with-logarithmic-scale-colorbar
# => norm=LogNorm(), ...but this doesn't work with 0 or negative values
def heatmap(data, title = None, subplots_adjust_parameters = None, xlabel = None, ylabel = None, **kwags):

  fig = px.imshow(data)

  fig.update_xaxes(
        tickangle = 45)
  fig.update_layout(
    autosize=True,
    margin=dict(l=0, r=0, t=25, b=10),
    title=title)
  
  return fig
