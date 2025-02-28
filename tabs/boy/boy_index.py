import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from maindash import app
from database import db_utility, graph_traces
import dash_bootstrap_components as dbc

df = db_utility.get_df()

year_options = [{'label':i,'value':i} for i in df['year'].unique()]
year_options.append({'label':'ALL','value':'ALL'})
year_val = 'ALL'
def year_value(value):
    if value == 'ALL':
        return df
    else:
        temp_df = df[df['year']==value]
        return temp_df

layout = html.Div([
    html.Div([
        html.H4('Year :'),
        dcc.Dropdown(
            id='year-dropdown',
            options=year_options,
            clearable=False,
            value='ALL'
        )], style={'width':'20%','display':'inline-block'}),

    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    'Product',
                    html.Hr(),
                ]),
                html.Div([
                    html.H2(id='top-boy-product')
                ])
            ])
        ], style={'border':'2px solid pink',
               'border-radius':10,
               'height':'10%',
               'width':'20%',
               'textAlign':'center',
               'paddingTop':'1%', 'display':'inline-block'}, width=2),

        dbc.Col([
            html.Div([
                html.Div([
                    'Brand',
                    html.Hr(),
                ]),
                html.Div([
                    html.H2(id='top-boy-brand')
                ])
            ])
        ], style={'border':'2px solid pink',
               'border-radius':10,
               'height':'10%',
               'width':'20%',
               'textAlign':'center',
               'paddingTop':'1%', 'display':'inline-block'}, width={'size':2, 'offset':1}),

        dbc.Col([
            html.Div([
                html.Div([
                    'Size',
                    html.Hr(),
                ]),
                html.Div([
                    html.H2(id='top-boy-size')
                ])
            ])
        ], style={'border':'2px solid pink',
               'border-radius':10,
               'height':'10%',
               'width':'20%',
               'textAlign':'center',
               'paddingTop':'1%', 'display':'inline-block'}, width={'size':2, 'offset':1}),

        dbc.Col([
            html.Div([
                html.Div([
                    'QTY.',
                    html.Hr(),
                ]),
                html.Div([
                    html.H2(id='top-boy-qty')
                ])
            ])
        ], style={'border':'2px solid pink',
               'border-radius':10,
               'height':'10%',
               'width':'20%',
               'textAlign':'center',
               'paddingTop':'1%', 'display':'inline-block'}, width={'size':2, 'offset':1}),

    ], style={'paddingTop':'2%'}),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='boy-items-bar-graph')
        ])
    ])
])

def Boy_Index():
    return layout

@app.callback(Output('top-boy-product','children'),
            [Input('year-dropdown','value')])
def update_product(value):
    top_val = db_utility.get_top_product(value, 'boy')
    return top_val

@app.callback(Output('top-boy-brand','children'),
            [Input('year-dropdown','value')])
def update_product(value):
    top_val = db_utility.get_top_brand(value, 'boy')
    return top_val

@app.callback(Output('top-boy-size','children'),
             [Input('year-dropdown','value')])
def update_size(value):
    top_val = db_utility.get_top_size(value,'boy')
    return top_val

@app.callback(Output('top-boy-qty','children'),
             [Input('year-dropdown','value')])
def update_qty(value):
    top_val = db_utility.get_top_qty(value,'boy')
    return top_val

@app.callback(Output('boy-items-bar-graph','figure'),
             [Input('year-dropdown','value')])
def update_male_item_bar_graph(value):
    return {'data':graph_traces.timeframe_wise_item_traces(value,'boy'),
            'layout': go.Layout(title='Boy Item Sales QTY.')}

if __name__ == '__main__':
    app.run_server()
