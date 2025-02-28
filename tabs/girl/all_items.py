import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from maindash import app
from database import db_utility, graph_traces

dropdown_options = [{'label':'Current Month','value':'1'},
                    {'label':'Last 2 Months','value':'2'},
                    {'label':'6 Months','value':'6'},
                    {'label':'Year','value':'12'},
                    ]

layout = html.Div([
        dbc.Row([
            dbc.Col([
                html.H4('Select Timeframe :'),
                dcc.Dropdown(
                    id='timeframe-dropdown',
                    options=dropdown_options,
                    clearable=False,
                    value='1',
                    style={'width':220}
                ),
            ])
        ]),
        dbc.Row(
            dbc.Col(
                #html.Div(id='all-item-graph')
                dcc.Graph(id='girl-all-item-graph')
            )
        ),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='girl-all-item-piechart')
            , width=5),
            dbc.Col(
                dcc.Graph(id='girl-all-item-barchart')
            )
        ])
])

def Girl_All_Items():
    return layout

@app.callback(Output('girl-all-item-graph','figure'),
             [Input('timeframe-dropdown','value')])
def update_graph(value):
    if (value=='1') | (value=='2'):
        return {'data':graph_traces.timeframe_all_items_traces(value,'girl','day'),
                'layout': go.Layout(title='All Girl Item Sales')}
    else:
        return {'data':graph_traces.timeframe_all_items_traces(value,'girl','month'),
                'layout': go.Layout(title='All Girl Item Sales')}

@app.callback(Output('girl-all-item-piechart','figure'),
             [Input('timeframe-dropdown','value')])
def update_piechart(value):
    final_df = db_utility.get_all_items_by_timeframe(value,'girl')
    if (value=='1') | (value=='2'):
        return {'data':[
              go.Pie(
                  labels=final_df['day'],
                  values=final_df['QTY.'],
                  hole=.3
                  )
              ],
              'layout': go.Layout(title='Sales Graph', margin={'b':0}, showlegend=False)}
    else:
        return {'data':[
              go.Pie(
                  labels=final_df['month'],
                  values=final_df['QTY.'],
                  hole=.3
                  )
              ],
              'layout': go.Layout(title='Sales Graph', margin={'b':0}, showlegend=False)}

@app.callback(Output('girl-all-item-barchart','figure'),
              [Input('timeframe-dropdown','value')])
def update_item_barchart(value):
    return {'data':graph_traces.timeframe_all_item_bar_traces(value,'girl'),
            'layout': go.Layout(title='All Girl Item Sales',uniformtext_minsize=10,
            uniformtext_mode='hide', showlegend=False)}

if __name__ == '__main__':
    app.run_server()
