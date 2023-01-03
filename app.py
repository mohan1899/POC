

#from dash import dcc
import dash_deck
import pydeck as pdk
import geopandas as gpd
import dash

import pandas as pd

from datetime import date

import dash_bootstrap_components as dbc

from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, html,State,dcc

from plotly.graph_objs import *
from datetime import datetime as dt
import calculation_fun as cf
#from plotly.subplots import make_subplots
import dash_auth


# get data from geoJson file
def read_map_df(path):
    
    geo_map_df = gpd.read_file(path)
    map_df = gpd.GeoDataFrame()
    map_df["name"] = geo_map_df.FID
    map_df["geometry"] = geo_map_df.geometry
    map_df["distance"] = geo_map_df.distance_value

    if str(geo_map_df.map_type[0]) == "Closure":
        color = [50,168,82] 
        color_list = [color]*len(map_df["name"])
        map_df["color"] = color_list
    elif str(geo_map_df.map_type[0]) == "Detour":
        color = [209,42,33] 
        color_list = [color]*len(map_df["name"])
        map_df["color"] = color_list
    return map_df
    





# create a layer for the map
def get_deck(map_data_df,closure_layout_data,detour_layout_data):
    #print(map_data_df)
    #print(closure_layout_data)
    #print(detour_layout_data)
    # Set the viewport location
    view_state = pdk.ViewState(latitude=-36.859067426240394, longitude=174.76020812611904, zoom=12)

    # Define a layer to display on a map
    base_layout = pdk.Layer(
        type = "PathLayer",
        data = map_data_df,
        pickable = True,
        get_color="color",
        width_scale = 2.5,
        width_min_pixels = 2,
        get_path = "geometry.coordinates",
        get_width = 3,
    )
    closure_layout= pdk.Layer(
        type = "PathLayer",
        data = closure_layout_data,
        pickable = True,
        get_color="color",
        width_scale = 2.5,
        width_min_pixels = 2,
        get_path = "geometry.coordinates",
        get_width = 4,
    )
    detour_layout = pdk.Layer(
        type = "PathLayer",
        data = detour_layout_data,
        pickable = True,
        get_color="color",
        width_scale = 2.5,
        width_min_pixels = 2,
        get_path = "geometry.coordinates",
        get_width = 4,
    )
    # Render
    # Start building the layout here
    r = pdk.Deck(layers=[base_layout,closure_layout,detour_layout], initial_view_state=view_state,map_provider='mapbox',map_style=pdk.map_styles.CARTO_DARK)
    return r

# Update color for the seleted path
def update_color(h):
    return[70,88,219]

total_number_lanes = 0

# closure_data_df = read_map_df("data/Closure_2.geojson") # map data set
# detour_data_df = read_map_df("data/Detour_2.geojson") # map data set

# original_block_closure_data_df = read_map_df("data/Block_Closure2.geojson") # map data set
# original_block_detour_data_df = read_map_df("data/Block_Detour2.geojson") # map data set

# original_closure_data_df = read_map_df("data/Closure_2.geojson") # map data set
# original_detour_data_df = read_map_df("data/Detour_2.geojson") # map data set


# site_id_df = pd.read_csv("data/site_id_lookup.csv")
# original_site_id_df = pd.read_csv("data/site_id_lookup.csv")
# # original_site_id_df = original_site_id_df[original_site_id_df["Ramp/Mainline"] == "Mainline"]
# site_id_df = site_id_df[site_id_df["Ramp/Mainline"] == "Mainline"]

# seasonal_data_df = pd.read_csv("data/Seasonal Data.csv", index_col=False)
# profile_label = pd.read_csv("data/profile_label2.csv")
# cluster_parameter = pd.read_csv(f"data/Cluster_Sites_Params.csv", index_col=False)
# detour_plan = pd.read_csv(f"data/detour_plan.csv")

#siteblock_list =list(site_id_df["Site Block"].values)
#closure_data_df = closure_data_df[closure_data_df["name"].isin(siteblock_list)]
#detour_data_df = detour_data_df[detour_data_df["name"].isin(siteblock_list)]
#road_name = list(set(closure_data_df["name"]))

drop_box_option = ['1','2'] 
SH_number = ["SH1","SH16","SH18","SH20","SH20A","SH20B","SH22"]
mapbox_api_token = "pk.eyJ1Ijoicml2aW5kdSIsImEiOiJjazZpZXo0amUwMGJ1M21zYXpzZGMzczdiIn0.eoArFYnhz0jEPQEnF0vdKQ" #For the base map token
list_of_data_lanes_number = ["1","2","3","4","5",]
   
start_time_option_list = ["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00",
                            "11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00",
                            "22:00","23:00"]

assets_path = "assets"

dash_app = dash.Dash(__name__)
VALID_USERNAME_PASSWORD_PAIRS = {
    'Ali': '1234',
    'Dan': "890"
}
dash_app = DashProxy(__name__, assets_folder = assets_path,prevent_initial_callbacks=True, transforms=[MultiplexerTransform()])
dash_app.title = "CIA Tool Development"
auth = dash_auth.BasicAuth(
    dash_app,
    VALID_USERNAME_PASSWORD_PAIRS
)
app = dash_app.server


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"



# Layout of Dash App
dash_app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.A(
                            html.Img(
                                className="logo",
                                src=dash_app.get_asset_url("Wsp_red.png"),
                            ),
                            href="https://www.wsp.com/en-nz/",
                        ),
                        html.H2("POC"),
                        html.Div(
                            dbc.Alert(
                                children = "",
                                id = "alert",
                                is_open = False,
                                color = "#f03508"

                            )

                        ),
                        html.P(
                            """Select closure locations from the dropdown or map."""
                        ),
                        html.Div(
                            
                            className="row",
                            children=[
                                html.Label("Closure Type:"),
                                html.Div(
                                dcc.RadioItems(id = "Closure_type", options= ['Block Closure', 'Single Closure'], value ='Single Closure', inline=True)
                                ),

                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        html.Label("Select SH Number(Option):"),
                                        dcc.Dropdown(
                                            id="drop_box_SH",
                                            options=SH_number,
                                            placeholder="Select SH Number",
                                            multi= False,
                                        )
                                    ],
                                ),
                            
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        html.Label("Select locations (Required):"),
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="drop_box_name",
                                            options=drop_box_option,
                                            placeholder="Select locations",
                                            multi= False,
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        html.Label("Select Number of Closed Lanes (Required):"),
                                        dcc.Dropdown(
                                            id="closed_lanes",
                                            options=[
                                                # {"label": i, "value": i}
                                                # for i in list_of_data_lanes_number
                                            ],
                                            placeholder="Select Number of Closed Lanes",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        html.Label("Select Closure Dates (Required):"),
                                        dcc.DatePickerSingle(
                                            id="date_picker",
                                            min_date_allowed=dt(2022, 1, 1),
                                            max_date_allowed=dt(2030, 12, 30),
                                            initial_visible_month= date.today(),
                                            # date=dt(2022, 10, 11).date(),
                                            placeholder="Select Closure Date",
                                            display_format="MMMM D, YYYY",
                                            style={"border": "0px solid black"},
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        html.Label("Select Start Time (Required):"),
                                        dcc.Dropdown(
                                            id="start_time",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in start_time_option_list
                                            ],
                                            multi=False,
                                            placeholder="Select Start Time",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        html.Label("Select End Time (Required):"),
                                      
                                        # dcc.Input(id="input2", type="time",step = 3600 ,placeholder="", debounce=True),
                                        dcc.Dropdown(
                                            id="end_time",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in start_time_option_list
                                            ],
                                            multi=False,
                                            placeholder="Select End Time",
                                            
                                        )
                                    ],
                                ),
                            ],
                        ),   
                        html.Button("calculation", id="calculation_btn", n_clicks=0),                  

                        # dcc.Markdown(
                        #     """
                        #     Data Source: [Download](https://github.com/fivethirtyeight/uber-tlc-foil-response/tree/master/uber-trip-data)

                        #     """
                        # ),
                    ],
                ),
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        html.Div(
                            id='map_container',
                            style={
                                "width": "100%",
                                "height": "70%",
                                "float": "left",
                                "display": "inline-block",
                                "position": "relative",
                            },
                            children=[
                                dash_deck.DeckGL(
                                    get_deck({},None,None).to_json(), # div section for map display
                                    id="deck_map",
                                    tooltip={"text": "{name}"},
                                    mapboxKey = mapbox_api_token,
                                    enableEvents=['click']
                                )
                            
                            ],
                        ),
                        html.Div(
                            className="eight columns div-for-charts bg-grey",
                            children=[
                               
                                html.Div(
                                    id='graph_container',
                                    style={
                                        "width": "155%",
                                        "height": "1vh",
                                        "right": "6.5%",
                                        "float": "left",
                                        "display": "inline-block",
                                        "position": "relative",
                                        
                                    },
                                    children = [
                                        dcc.Tabs(
                                            colors ={"border": "black"},
                                            #content_style={"background-color": " rgb(9, 80, 124)"},
                                            id="tabs_graph",
                                            value='detour_graph', 
                                            children=[
                                            dcc.Tab(label='Detour Route', value='detour_graph',children=[
                                                dcc.Graph(
                                                id = "histogram2",
                                                figure = {
                                                "layout": {
                                                "paper_bgcolor" : "#111111",
                                                "plot_bgcolor":"#111111",
                                                'font': {
                                                    'color': "#111111"
                                                    }
                                                }
                                                }
                                                ),

                                            ]),
                                            dcc.Tab(label='Closure Route', value='closure_graph',children=[
                                                dcc.Graph(
                                                id = "histogram",
                                                figure = {
                                                        "layout": {
                                                        "paper_bgcolor" : "#111111",
                                                        "plot_bgcolor":"#111111",
                                                        'font': {
                                                            'color': "#111111"
                                                                },
                                                        
                                                        
                                                                },
                                                        

                                                            },
                            
                                                
                                                    )

                                            ]),
                                            
                                            
                                        ]
                                        ),
                                        
                                        
                                        ]
                                )
                                
                                # dcc.Graph(id="histogram"),
                            ],
                        ),                 
                        # dcc.Graph(id="map-graph"),
                        # html.Div(
                        #     className="text-padding",
                        #     children=[
                        #         "Select any locations from the map."
                        #     ],
                        # ),
                        # dcc.Graph(id="histogram"),
                    ],
                ),
                # html.Div(
                #     className="eight columns div-for-charts bg-grey",
                #     children=[
                #         html.Div(
                #             id='graph_container',
                #             style={
                #                 "width": "100%",
                #                 "height": "55vh",
                #                 "float": "left",
                #                 "display": "inline-block",
                #                 "position": "relative",
                #             },
                #             children = [
                #                 dcc.Graph(id = "histogram"),
                #                 dcc.Graph(id = "histogram2")
                #                 ]
                #         )
                           
                #         # dcc.Graph(id="histogram"),
                #     ],
                # ),
            ],
        )
    ]
)

@dash_app.callback(
    Output("map_container","children"),
    [Input("drop_box_name","options"),State("Closure_type","value")],
    prevent_initial_call=True,
)
def update_map_road_data(options,Closure_type):
    print(options)
    #print(options)
    global closure_data_df,detour_data_df,original_closure_data_df,original_detour_data_df, original_block_closure_data_df, original_block_detour_data_df
    if Closure_type == "Block Closure":
        closure_data_df = original_block_closure_data_df[original_block_closure_data_df["name"].isin(options)]
        detour_data_df = original_block_detour_data_df[original_block_detour_data_df["name"].isin(options)]
        return dash_deck.DeckGL(
                            get_deck(closure_data_df,None,None).to_json(),
                            id = "deck_map",
                            tooltip = {"text": "{name}"}, 
                            mapboxKey = mapbox_api_token,
                            enableEvents=['click']
                        )


    elif Closure_type == "Single Closure":
        closure_data_df = original_closure_data_df[original_closure_data_df["name"].isin(options)]
        detour_data_df = original_detour_data_df[original_detour_data_df["name"].isin(options)]
        return dash_deck.DeckGL(
                            get_deck(closure_data_df,None,None).to_json(),
                            id = "deck_map",
                            tooltip = {"text": "{name}"}, 
                            mapboxKey = mapbox_api_token,
                            enableEvents=['click']
                        )



@dash_app.callback(
    [Output("drop_box_name","options"),Output("drop_box_name","value")],
    Input("drop_box_SH" , "value"),
    prevent_initial_call=True,
)
def updat_drop_box_road_name(value):
    global site_id_df
    #print("check",site_id_df)
    
    if value != None:
        
        options = site_id_df[site_id_df["Site Block"].str.contains(f"^{value}_.*|^{value}_.*")]
        options = list(options["Site Block"].values)
        return options,None

        
    else:
        drop_box_option = [roadid for roadid in set(list(site_id_df["Site Block"].values))] 
        #print(drop_box_option)
        return drop_box_option,None


@dash_app.callback(
    [Output("map_container","children"),Output("drop_box_SH","value"),Output("closed_lanes","value")],
    Input("Closure_type","value"),
    prevent_initial_call=True,
)
def change_map_type(value):
    global original_block_closure_data_df, original_block_detour_data_df, original_closure_data_df, original_detour_data_df, closure_data_df, detour_data_df, site_id_df,original_site_id_df
    if value == "Block Closure":
        closure_data_df = original_block_closure_data_df[original_block_closure_data_df["name"].isin(siteblock_list)]
        detour_data_df = original_block_detour_data_df[original_block_detour_data_df["name"].isin(siteblock_list)]
        site_id_df = original_site_id_df[original_site_id_df["Site Block"].str.contains(f"^.* .*")]
        site_id_df = site_id_df[site_id_df["Ramp/Mainline"] == "Mainline"]
        #print(site_id_df)
        map_container = dash_deck.DeckGL(
                        get_deck(closure_data_df,None,None).to_json(),
                        id = "deck_map",
                        tooltip = {"text": "{name}"}, 
                        mapboxKey = mapbox_api_token,
                        enableEvents=['click']
                    )
        
        return map_container,None,None
    elif value == "Single Closure":
        closure_data_df = original_closure_data_df[original_closure_data_df["name"].isin(siteblock_list)]
        detour_data_df = original_detour_data_df[original_detour_data_df["name"].isin(siteblock_list)]
        site_id_df = original_site_id_df[original_site_id_df["Site Block"].str.contains(f"^.*_.*")]
        site_id_df = site_id_df[site_id_df["Ramp/Mainline"] == "Mainline"]
        #print(site_id_df)
        map_container = dash_deck.DeckGL(
                        get_deck(closure_data_df,None,None).to_json(),
                        id = "deck_map",
                        tooltip = {"text": "{name}"}, 
                        mapboxKey = mapbox_api_token,
                        enableEvents=['click']
                    )
        return map_container,None,None


@dash_app.callback(
    [Output("closed_lanes","options"),Output("closed_lanes","value")],
    [Input('drop_box_name','value'),State("closed_lanes","value"),State("closed_lanes","options")],
    prevent_initial_call=True,
)
def update_lanes(value,closed_lanes_value,closed_lanes_options):

    global total_number_lanes
    #print(value)
    #print(value)
    try:
        if value != None and value != "":
            if closed_lanes_value != None and closed_lanes_value != "":
                return closed_lanes_options,closed_lanes_value

            else:
                data =  site_id_df[site_id_df["Site Block"] == value]
                lane = int(data["Number of Lane(s)"].values[0])
                options = [i+1 for i in range(lane)]
                total_number_lanes = lane
                return options,None
        else:
            return [],None
    except:
        return [],None




@dash_app.callback(
    Output('map_container','children'),
    [Input('drop_box_name','value'),State('map_container','children')],
    prevent_initial_call=True,
)
def update_graph(value,map):
    global closure_layout_data,detour_layout_data
    try:
        if value == None or value ==[]:
            return dash_deck.DeckGL(
                        get_deck(closure_data_df,None,None).to_json(),
                        id = "deck_map",
                        tooltip = {"text": "{name}"}, 
                        mapboxKey = mapbox_api_token,
                        enableEvents=['click']
                    )
        else:
            closure_layout_data = gpd.GeoDataFrame()
            detour_layout_data = gpd.GeoDataFrame()

            closure_value = closure_data_df[closure_data_df.name == value]
            closure_value["color"] =  closure_value["color"].apply(update_color)
            
            detour_value = detour_data_df[detour_data_df.name == value]
            
        
            closure_layout_data = closure_layout_data.append(closure_value,ignore_index  = True)
            detour_layout_data = detour_layout_data.append(detour_value, ignore_index = True)
            
                
        
            return dash_deck.DeckGL(
                        get_deck(closure_data_df,closure_layout_data,None).to_json(),
                        id = "deck_map",
                        tooltip = {"text": "{name}"}, 
                        mapboxKey = mapbox_api_token,
                        enableEvents=['click']
                    )
    except:
        return map

#call back fuction for updating drop down box
    

@dash_app.callback(
    Output("drop_box_name","value"),
    [Input("deck_map","clickInfo"), State("drop_box_name","value")],
    prevent_initial_call=True,
    )

def update_drop_box(clickInfo,value):
    
    try:
        if (value == None or value == "" )and clickInfo == None:
            return None
        elif clickInfo !=None:
            return str(clickInfo["object"]["name"])
        elif value != None or value != "":
            return value
        else:
            return str(clickInfo["object"]["name"])
    except:
        return value

@dash_app.callback(
    [Output("histogram","figure"),Output("histogram2","figure"),Output("alert","is_open"),Output("alert","children"),Output("tabs_graph","value"),Output('map_container','children')],
    [Input("calculation_btn","n_clicks"),State("drop_box_name","value"),State("closed_lanes","value"),State("date_picker","date"),State("start_time","value"),State("end_time","value"),State("histogram","figure"),State("histogram2","figure"),State('map_container','children')],
    prevent_initial_call=True,
)
def create_histogram(n_clicks,road_name,closed_lanes,closure_date,start_time,end_time,graph1,graph2,map):
   
    global original_site_id_df,seasonal_data_df,profile_label,detour_layout_data,closure_layout_data
    try:
        graph1,graph2 = cf.run(road_name,start_time,end_time,closed_lanes,original_site_id_df,seasonal_data_df,profile_label,closure_date,cluster_parameter,detour_plan)
        show_tab = "closure_graph"
        map = dash_deck.DeckGL(
                        get_deck(closure_data_df,closure_layout_data,None).to_json(),
                        id = "deck_map",
                        tooltip = {"text": "{name}"}, 
                        mapboxKey = mapbox_api_token,
                        enableEvents=['click']
                    )
        
        if total_number_lanes == closed_lanes:
            show_tab = "detour_graph"
            
            map = dash_deck.DeckGL(
                        get_deck(closure_data_df,closure_layout_data,detour_layout_data).to_json(),
                        id = "deck_map",
                        tooltip = {"text": "{name}"}, 
                        mapboxKey = mapbox_api_token,
                        enableEvents=['click']
                    )
       
        return graph1,graph2,False,"",show_tab,map
    except Exception as e:
        if road_name == None or closed_lanes == None or closure_date == None or start_time == None or end_time == None:
            msg = "Plase Check your parameters"
        else:
            msg = f"The road id is not available yet, please try it later."
        return graph1,graph2,True,msg,"detour_graph",map
    #print(road_name,closed_lanes,closure_date,start_time,end_time)
    # print(n_clicks,road_name,closed_lanes,closure_date,start_time,end_time)
    # print(cf.run(road_name,start_time,end_time,closed_lanes))
    # fig = make_subplots(rows=1, cols=2)
    # fig = make_subplots(rows=1, cols=2)
    # fig.add_trace(
    # go.Scatter(x=[1, 2, 3], y=[4, 5, 6]),
    # row=1, col=1)
    # fig.add_trace(go.Scatter(x=[20, 30, 40], y=[50, 60, 70]),row=1, col=2)

    #print(profile_label)
    #print(road_name,closed_lanes,closure_date,start_time,end_time)

    #print("original_site_id_df")
    #print(original_site_id_df)

    #print("seasonal_data_df")
    #print(seasonal_data_df)
    #print("profile_label")
    #print(profile_label)
    


    # return cf.run(road_name,start_time,end_time,closed_lanes,original_site_id_df,seasonal_data_df,profile_label,closure_date,cluster_parameter,detour_plan)

if __name__ == "__main__":
    dash_app.run_server(port= 8080)
