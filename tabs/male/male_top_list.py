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

male_item_options = db_utility.get_all_items_dropdown('male')

layout = html.Div([

    ################################------- TOP MALE ITEM LAYOUT ---------#################################
    dbc.Row([
        dbc.Col([
            html.H3('Top Male Item analysis')
        ], width={'size':'100%'})
    ],justify="center"),

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
            html.Div(id='top-list-table')
        ], align="start", width={'size':4}),

        dbc.Col(
            dcc.Graph(id='top-male-items')
        , width={'size':8})
    ], justify="around"),

    ################################## ------------- BRAND WISE LAYOUT --------- ###########################

    dbc.Row(dbc.Col(dcc.Graph(id='item-brand-graph'))),

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
                id='items-dropdown',
                options=male_item_options,
                clearable=False,
                value='M.BRIEF',
                style={'width':220}
            ),
            html.Div(id='range-list-table'),
            html.Br(),
            html.Div(id='range-list-click-data')
        ], align="start", width={'size':4}),

        dbc.Col(
            dcc.Graph(id='rangewise-male-items')
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
                id='male-items',
                options=male_item_options,
                clearable=False,
                value='M.BRIEF',
                style={'width':220}
            ),
            html.Div(id='sizewise-male-table')
        ], align="start", width={'size':4}),

        dbc.Col(
            dcc.Graph(id='sizewise-male-items')
        , width={'size':8})
    ], justify="around")
])

def Male_Top_List():
    return layout

#########------ TOP MALE Item CallBack ------##########
@app.callback(Output('top-list-table','children'),
             [Input('timeframe-dropdown','value')])
def update_table(value):
        final_df = db_utility.df_timeframe(value,'male')
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

@app.callback(Output('top-male-items','figure'),
            [Input('timeframe-dropdown','value')])
def update_graph(value):
    return {'data':graph_traces.timeframe_traces(value,'male'),
            'layout': go.Layout(title='Top Male Item Sales')}


#########------ BRAND Wise Male Item CallBack--------#########

@app.callback(Output('item-brand-graph','figure'),
            [Input('timeframe-dropdown','value'),
            Input('top-male-items','clickData')])
def brand_graph_click_data(value,clickData):
    if clickData is None:
        return {'data':graph_traces.brandwise_items_traces(value, 'M.TSHIRT', 'male'),
                'layout': go.Layout(title='Click on Above Graph to check Brands of Item')}
    else:
        item_data = clickData['points'][0]['x']
        return {'data':graph_traces.brandwise_items_traces(value, item_data, 'male'),
                'layout': go.Layout(title='{}'.format(item_data))}
        #return json.dumps(item_data)

#########------ RANGE Wise Male Item CallBack ------##########

@app.callback(Output('range-list-table','children'),
             [Input('timeframe-dropdown','value'),
             Input('items-dropdown','value')])
def rangewise_update_table(timeframe, value):
        final_df = db_utility.add_range_df(timeframe,value,'male')
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

@app.callback(Output('rangewise-male-items','figure'),
            [Input('timeframe-dropdown','value'),
            Input('items-dropdown','value')])
def update_sizewise_graph(timeframe_val,value):
    return {'data':graph_traces.rangewise_items_traces(timeframe_val,value,'male'),
            'layout': go.Layout(title='Range wise Item LIST'.format(value))}

@app.callback(Output('range-list-click-data','children'),
            [Input('timeframe-dropdown','value'),
            Input('items-dropdown','value'),
            Input('rangewise-male-items','clickData')])
def range_graph_click_data(timeframe_val,value,clickData):
    if clickData is None:
        return 'Click on Graph Data to see More in detail..'
    else:
        weightage = clickData['points'][0]['x']
        temp_df = db_utility.get_weightage_top_list(timeframe_val,value, 'male', weightage)
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

@app.callback(Output('sizewise-male-table','children'),
             [Input('timeframe-dropdown','value'),
             Input('male-items','value')])
def sizewise_update_table(timeframe_val, value):
        final_df = db_utility.sizewise_items_list(timeframe_val,value,'male')
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

@app.callback(Output('sizewise-male-items','figure'),
            [Input('timeframe-dropdown','value'),
            Input('male-items','value')])
def update_sizewise_graph(timeframe_val,value):
    return {'data':graph_traces.sizewise_items_traces(timeframe_val,value,'male'),
            'layout': go.Layout(title='Top Size of {} Item'.format(value))}
