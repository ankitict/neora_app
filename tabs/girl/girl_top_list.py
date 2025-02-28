import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from datetime import datetime
import numpy as np
import json
from maindash import app
import dash_table
import dash_bootstrap_components as dbc
from database import db_utility
from database import graph_traces

df = db_utility.get_df()

dropdown_options = [{'label':'Current Month','value':'1'},
                    {'label':'Last 2 Months','value':'2'},
                    {'label':'6 Months','value':'6'},
                    {'label':'Year','value':'12'},
                    ]

girl_item_options = db_utility.get_all_items_dropdown('girl')

layout = html.Div([

    ################################------- TOP GIRL ITEM LAYOUT ---------#################################
    dbc.Row([
        dbc.Col([
            html.H3('Top Girl Item analysis')
        ], width={'size':'100%'})
    ],justify="center"),

    dbc.Row([
        dbc.Col([
            html.H4('Select Timeframe :'),
            dcc.Dropdown(
                id='timeframe-dropdown-girl',
                options=dropdown_options,
                clearable=False,
                value='1',
                style={'width':220}
            ),
            html.Br(),
            html.Div(id='top-list-table-girl')
        ], align="start", width={'size':4}),

        dbc.Col(
            dcc.Graph(id='top-girl-items')
        , width={'size':8})
    ], justify="around"),

    ################################## ------------- BRAND WISE LAYOUT --------- ###########################

    dbc.Row(dbc.Col(dcc.Graph(id='girl-item-brand-graph'))),

    ################################------- SIZE WISE ITEM LAYOUT ---------#################################

    dbc.Row([
        dbc.Col([
            html.H3('Size wise analysis')
        ], width={'size':'100%'})
    ],justify="center"),

    dbc.Row([
        dbc.Col([
            html.H4('Select Item :'),
            dcc.Dropdown(
                id='girl-items',
                options=girl_item_options,
                clearable=False,
                value='G.NIGHTSUIT',
                style={'width':220}
            ),
            html.Div(id='sizewise-girl-table')
        ], align="start", width={'size':4}),

        dbc.Col(
            dcc.Graph(id='sizewise-girl-items')
        , width={'size':8})
    ], justify="around")
])

def Girl_Top_List():
    return layout

#########------ TOP MALE Item CallBack ------##########
@app.callback(Output('top-list-table-girl','children'),
             [Input('timeframe-dropdown-girl','value')])
def update_table(value):
        final_df = db_utility.df_timeframe(value,'girl')
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

                } for c in ['PRODUCT NAME']
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

@app.callback(Output('top-girl-items','figure'),
            [Input('timeframe-dropdown-girl','value')])
def update_graph(value):
    return {'data':graph_traces.timeframe_traces(value,'girl'),
            'layout': go.Layout(title='Top Girl Item Sales')}

#########------ BRAND Wise Girl Item CallBack--------#########

@app.callback(Output('girl-item-brand-graph','figure'),
            [Input('timeframe-dropdown-girl','value'),
            Input('top-girl-items','clickData')])
def brand_graph_click_data(value,clickData):
    if clickData is None:
        return {'data':graph_traces.brandwise_items_traces(value, 'G.NIGHTSUIT', 'girl'),
                'layout': go.Layout(title='Click on Above Graph to check Brands of Item')}
    else:
        item_data = clickData['points'][0]['x']
        return {'data':graph_traces.brandwise_items_traces(value, item_data, 'girl'),
                'layout': go.Layout(title='{}'.format(item_data))}


#########------ SIZE Wise Male Item CallBack ------##########

@app.callback(Output('sizewise-girl-table','children'),
             [Input('timeframe-dropdown-girl','value'),
             Input('girl-items','value')])
def sizewise_update_table(timeframe, value):
        final_df = db_utility.sizewise_items_list(timeframe, value,'girl')
        return html.Div([
			dash_table.DataTable(
				id='size_table',
				columns=[{"name": i, "id": i} for i in final_df.columns],
				data=final_df.to_dict("rows"),
                style_table={'width': '25%', 'paddingLeft':'20%',
                            'paddingTop':'2%', 'display':'inline-block'},
				style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'left',

                } for c in ['SIZE']
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

@app.callback(Output('sizewise-girl-items','figure'),
            [Input('timeframe-dropdown-girl','value'),
            Input('girl-items','value')])
def update_sizewise_graph(timeframe, value):
    return {'data':graph_traces.sizewise_items_traces(timeframe, value,'girl'),
            'layout': go.Layout(title='Top Size of {} Item'.format(value))}

if __name__ == '__main__':
    app.run_server(debug=True)
