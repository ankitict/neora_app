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

boy_item_options = db_utility.get_all_items_dropdown('boy')

layout = html.Div([

    ################################------- TOP BOY ITEM LAYOUT ---------#################################
    dbc.Row([
        dbc.Col([
            html.H3('Top Boy Item analysis')
        ], width={'size':'100%'})
    ],justify="center"),

    dbc.Row([
        dbc.Col([
            html.H4('Select Timeframe :'),
            dcc.Dropdown(
                id='timeframe-dropdown-boy',
                options=dropdown_options,
                clearable=False,
                value='1',
                style={'width':220}
            ),
            html.Br(),
            html.Div(id='top-list-table-boy')
        ], align="start", width={'size':4}),

        dbc.Col(
            dcc.Graph(id='top-boy-items')
        , width={'size':8})
    ], justify="around"),

    ################################## ------------- BRAND WISE LAYOUT --------- ###########################

    dbc.Row(dbc.Col(dcc.Graph(id='boy-item-brand-graph'))),


    ################################------- RANGE WISE ITEM LAYOUT ---------#################################

    dbc.Row([
        dbc.Col([
            html.H3('Top Selling Range analysis')
        ], width={'size':'100%'})
    ],justify="center"),

    dbc.Row([
        dbc.Col([
            html.H4('Select Item :'),
            dcc.Dropdown(
                id='boy-items-dropdown',
                options=boy_item_options,
                clearable=False,
                value='B.NIGHTSUIT',
                style={'width':220}
            ),
            html.Div(id='boy-range-list-table'),
            html.Br(),
            html.Div(id='boy-range-list-click-data')
        ], align="start", width={'size':4}),

        dbc.Col(
            dcc.Graph(id='rangewise-boy-items')
        , width={'size':8})
    ], justify="around"),

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
                id='boy-items',
                options=boy_item_options,
                clearable=False,
                value='B.NIGHTSUIT',
                style={'width':220}
            ),
            html.Div(id='sizewise-boy-table')
        ], align="start", width={'size':4}),

        dbc.Col(
            dcc.Graph(id='sizewise-boy-items')
        , width={'size':8})
    ], justify="around")
])

def Boy_Top_List():
    return layout

#########------ TOP MALE Item CallBack ------##########
@app.callback(Output('top-list-table-boy','children'),
             [Input('timeframe-dropdown-boy','value')])
def update_table(value):
        final_df = db_utility.df_timeframe(value,'boy')
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

@app.callback(Output('top-boy-items','figure'),
            [Input('timeframe-dropdown-boy','value')])
def update_graph(value):
    return {'data':graph_traces.timeframe_traces(value,'boy'),
            'layout': go.Layout(title='Top Boy Item Sales')}

#########------ BRAND Wise Boy Item CallBack--------#########

@app.callback(Output('boy-item-brand-graph','figure'),
            [Input('timeframe-dropdown-boy','value'),
            Input('top-boy-items','clickData')])
def brand_graph_click_data(value,clickData):
    if clickData is None:
        return {'data':graph_traces.brandwise_items_traces(value, 'B.TSHIRT', 'boy'),
                'layout': go.Layout(title='Click on Above Graph to check Brands of Item')}
    else:
        item_data = clickData['points'][0]['x']
        return {'data':graph_traces.brandwise_items_traces(value, item_data, 'boy'),
                'layout': go.Layout(title='{}'.format(item_data))}


#########------ RANGE Wise Male Item CallBack ------##########

@app.callback(Output('boy-range-list-table','children'),
             [Input('timeframe-dropdown-boy','value'),
             Input('boy-items-dropdown','value')])
def rangewise_update_table(timeframe, value):
        final_df = db_utility.add_range_df(timeframe, value,'boy')
        return html.Div([
			dash_table.DataTable(
				id='range_table',
				columns=[{"name": i, "id": i} for i in final_df.columns],
				data=final_df.to_dict("rows"),
                style_table={'width': '25%', 'paddingLeft':'20%',
                            'paddingTop':'2%', 'display':'inline-block'},
				style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'left',

                } for c in ['weightage']
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

@app.callback(Output('rangewise-boy-items','figure'),
            [Input('timeframe-dropdown-boy','value'),
            Input('boy-items-dropdown','value')])
def update_sizewise_graph(timeframe, value):
    return {'data':graph_traces.rangewise_items_traces(timeframe, value,'boy'),
            'layout': go.Layout(title='Range wise Item LIST'.format(value))}

@app.callback(Output('boy-range-list-click-data','children'),
            [Input('timeframe-dropdown-boy','value'),
            Input('boy-items-dropdown','value'),
            Input('rangewise-boy-items','clickData')])
def range_graph_click_data(timeframe, value,clickData):
    if clickData is None:
        return 'Click on Graph Data to see More in detail..'
    else:
        weightage = clickData['points'][0]['x']
        temp_df = db_utility.get_weightage_top_list(timeframe, value, 'boy', weightage)
        return html.Div([
			dash_table.DataTable(
				id='range_table1',
				columns=[{"name": i, "id": i} for i in temp_df.columns],
				data=temp_df.to_dict("rows"),
                style_table={'width': '25%', 'paddingLeft':'15%',
                            'paddingTop':'1%', 'display':'inline-block'},
				style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'left',

                } for c in ['weightage']
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




#########------ SIZE Wise Male Item CallBack ------##########

@app.callback(Output('sizewise-boy-table','children'),
             [Input('timeframe-dropdown-boy','value'),
             Input('boy-items-dropdown','value')])
def sizewise_update_table(timeframe, value):
        final_df = db_utility.sizewise_items_list(timeframe, value,'boy')
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

@app.callback(Output('sizewise-boy-items','figure'),
            [Input('timeframe-dropdown-boy','value'),
            Input('boy-items','value')])
def update_sizewise_graph(timeframe, value):
    return {'data':graph_traces.sizewise_items_traces(timeframe, value,'boy'),
            'layout': go.Layout(title='Top Size of {} Item'.format(value))}

if __name__ == '__main__':
    app.run_server(debug=True)
