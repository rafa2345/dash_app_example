
# coding: utf-8

# In[141]:

import dash
from dash.dependencies import Input, Output 
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


# In[143]:

#create the app:
#app = dash.Dash()
app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
#import the dataset from "http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp"
df= pd.read_csv("nama_10_gdp_Data.csv")

#choose one single unit
df=df[df['UNIT']=='Current prices, million euro'] 

#create NA_ITEMS and GEOS
NA_ITEMS=df.NA_ITEM.unique()

GEOS = df['GEO'].unique()

#FIRST, design the layout of the app

app.layout = html.Div([

#1.The first graph    

    html.Div([
#1.1 the first dropdown box of the first graph (this stuff it is done in the layout section)
        html.Div([
            dcc.Dropdown( 
                id='xaxisgraph1',
                options=[{'label': i, 'value': i} for i in NA_ITEMS],
                value='Final consumption expenditure'
            )
        ],
        style={'width': '30%', 'display': 'inline-block','color':'red'}),
#1.2 the second dropdown box for the first graph
        html.Div([
            dcc.Dropdown( 
                id='yaxisgraph1',
                options=[{'label': i, 'value': i} for i in NA_ITEMS],
                value='Gross capital formation'
            )
        ],style={'width': '30%', 'float': 'right', 'display': 'inline-block','color':'red'})
    ]),

#1.3 create the slider
    html.Div(dcc.Slider( 
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].min(),
        step=None,
        marks={str(time): str(time) for time in df['TIME'].unique()},
        
    ), style={'marginRight': 50, 'marginLeft': 190, 'marginTop':50, 'marginBottom':50},),
    
#1.4 Create the first graph itself
    dcc.Graph(id='graph1'),

#2. The second graph
    
    html.Div([
#2.1 The first dropdownbox of the second graph        
           html.Div([
            dcc.Dropdown( 

                id='xaxisgraph2',
                options=[{'label': i, 'value': i} for i in NA_ITEMS],
                value='Final consumption expenditure'
            )
        ],
        style={'width': '30%', 'marginTop': 40, 'display': 'inline-block','color':'red'}),
#2.2 The second dropdownbox of the second graph
        html.Div([
            dcc.Dropdown( 
                id='yaxisgraph2',
                options=[{'label': i, 'value': i} for i in GEOS],
                value= "Spain"
                
            )
        ],style={'width': '30%', 'marginTop': 40, 'float': 'right', 'display': 'inline-block','color':'red'})
     ]),
#2.3 create the second graph itself
     dcc.Graph(id='graph2'),


])

#3. Create the callback which updates the first graph according to the value in the dropdown boxes

@app.callback(
    dash.dependencies.Output('graph1', 'figure'),
    [dash.dependencies.Input('xaxisgraph1', 'value'),
     dash.dependencies.Input('yaxisgraph1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

#4. Define the function for the first graph
def update_graph1(xaxis_column_name, yaxis_column_name,
                 year_value):
#4.1 create the dataset with the year chosen 
    year_data = df[df['TIME'] == year_value]
#4.2 create the data with the inputs of the dropdown boxes.
    return {
        'data': [go.Scatter(
            x=year_data[year_data['NA_ITEM'] == xaxis_column_name]['Value'],
            y=year_data[year_data['NA_ITEM'] == yaxis_column_name]['Value'],
            hovertext=year_data[year_data['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 90, 'b': 50, 't': 20, 'r': 50},
            hovermode='closest'
        )
    }

##5. Create the callback which updates the second graph according to the value in the dropdown boxes
@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('xaxisgraph2', 'value'),
     dash.dependencies.Input('yaxisgraph2', 'value')])

#6. Define the function for the second graph
def update_graph2(xaxis_column_name, yaxis_column_name):
#6.1 create the dataset with the country chosen     
    country_data = df[df['GEO'] == yaxis_column_name]

#6.2 create the linechart
    return {
        'data': [go.Scatter(
            x=country_data['TIME'].unique(),
            y=country_data[country_data['NA_ITEM'] == xaxis_column_name]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 90, 'b': 50, 't': 20, 'r': 50},
            hovermode='closest'
        )
    }

#7.Run the server

if __name__ == '__main__':
    app.run_server()


# In[ ]:



