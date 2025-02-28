import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from maindash import app
from database import db_utility, graph_traces

dropdown_options = [{'label':'Weekly','value':'7'},
                    {'label':'Monthly','value':'1'},
                    {'label':'6 Months','value':'6'},
                    {'label':'Yearly','value':'12'},
                    ]
male_item_options = db_utility.get_all_items_dropdown('male')

layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H5('Timeframe :'),
                dcc.Dropdown(
                    id='timeframe-dropdown',
                    options=dropdown_options,
                    clearable=False,
                    value='7',
                    style={'width':220}
                ),
            ], style={'paddingTop':'2%', 'paddingBottom':'2%'},width=3),
            dbc.Col([
                html.H5('Items :'),
                dcc.Dropdown(
                    id='items-dropdown',
                    options=male_item_options,
                    clearable=False,
                    value='M.BRIEF',
                    style={'width':220}
                ),
            ], style={'paddingTop':'2%', 'paddingBottom':'2%'}),
        ]),

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        'Product',
                        html.Hr(),
                    ]),
                    html.Div([
                        html.H2(id='top-male-item')
                    ])
                ])
            ], style={'border':'2px solid pink',
                   'border-radius':10,
                   'height':'10%',
                   'textAlign':'center',
                   'paddingTop':'1%',
                   'display':'inline-block'}, width=3),

            dbc.Col([
                html.Div([
                    html.Div([
                        'Qty.',
                        html.Hr(),
                    ]),
                    html.Div([
                        html.H2(id='male-item-qty')
                    ])
                ])
            ], style={'border':'2px solid pink',
                   'border-radius':10,
                   'height':'10%',
                   'textAlign':'center',
                   'paddingTop':'1%',
                   'display':'inline-block'}, width={'size':1, 'offset':1}),

            dbc.Col([
                html.Div([
                    html.Div([
                        'Brand',
                        html.Hr(),
                    ]),
                    html.Div([
                        html.H2(id='male-item-brand')
                    ])
                ])
            ], style={'border':'2px solid pink',
                   'border-radius':10,
                   'height':'10%',
                   'textAlign':'center',
                   'paddingTop':'1%',
                   'display':'inline-block'}, width={'size':3, 'offset':1}),

            dbc.Col([
                html.Div([
                    html.Div([
                        'Size',
                        html.Hr(),
                    ]),
                    html.Div([
                        html.H2(id='male-item-size')
                    ])
                ])
            ], style={'border':'2px solid pink',
                   'border-radius':10,
                   'height':'10%',
                   'width':'20%',
                   'textAlign':'center',
                   'paddingTop':'1%', 'display':'inline-block'}, width={'size':1, 'offset':1}),

        ], style={'paddingLeft':'1%'})

],style={"height": "100vh"})

def All_Items():
    return layout

@app.callback(Output('top-male-item','children'),
            [Input('items-dropdown','value')])
def set_product_name(value):
    val = value.split('.')[1]
    return val

@app.callback(Output('male-item-qty','children'),
            [Input('timeframe-dropdown','value'),
             Input('items-dropdown','value')])
def set_product_qty(timeframe, item):
    val = db_utility.items_qty(timeframe, item, 'male')
    return val

@app.callback(Output('male-item-brand','children'),
            [Input('timeframe-dropdown','value'),
             Input('items-dropdown','value')])
def set_product_brand(timeframe, item):
    val = db_utility.items_brand(timeframe, item, 'male')
    return val

@app.callback(Output('male-item-size','children'),
            [Input('timeframe-dropdown','value'),
             Input('items-dropdown','value')])
def set_product_size(timeframe, item):
    val = db_utility.items_size(timeframe, item, 'male')
    return val
