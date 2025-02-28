import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from datetime import datetime
import numpy as np
import json
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
            html.Br(),
            html.Div(id='top-brand-list-table')
        ], align="start", width={'size':4}),

        dbc.Col(
            dcc.Graph(id='top-brand-list-graph')
        , width={'size':8})
    ], justify="around")
])

def Male_Brand():
    return layout

@app.callback(Output('top-brand-list-table','children'),
             [Input('timeframe-dropdown','value')])
def update_table(value):
        final_df = db_utility.brand_timeframe(value,'male')
        return html.Div([
			dash_table.DataTable(
				id='table',
				columns=[{"name": i, "id": i} for i in final_df.columns],
				data=final_df.to_dict("rows"),
                style_table={'width': '25%', 'paddingLeft':'20%',
                            'paddingTop':'5%', 'display':'inline-block'},
				style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'left',

                } for c in ['BRAND']
                ],
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                })
			])

@app.callback(Output('top-brand-list-graph','figure'),
            [Input('timeframe-dropdown','value')])
def update_graph(value):
    return {'data':graph_traces.timeframe_brand_traces(value,'male'),
            'layout': go.Layout(title='Top Brand Sales')}

if __name__ == '__main__':
    app.run_server(debug=True)
