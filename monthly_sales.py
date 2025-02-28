import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from datetime import datetime
import numpy as np
from maindash import app
import dash_table
from database import sales_utility
from database import db_utility
import os

#app = dash.Dash()

df = sales_utility.get_df()
#df.set_index('DATE',inplace=True)

year_options = [{'label':i,'value':i} for i in df['year'].unique()]
year_options.append({'label':'ALL','value':'ALL'})
year_val = 'ALL'

cat_options = [{'label':i,'value':i} for i in df['item_type'].unique()]
cat_options.append({'label':'ALL','value':'ALL'})
cat_val = 'ALL'

body = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4('Year :'),
            dcc.Dropdown(
                id='year-dropdown',
                options=year_options,
                clearable=False,
                value='ALL'
            )], style={'display':'inline-block'}, width=2),

        dbc.Col([
            html.H4('Category :'),
            dcc.Dropdown(
                id='category-dropdown',
                options=cat_options,
                clearable=False,
                value='ALL'
            ),
            ], style={'display':'inline-block'}, width=2),
        ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='pie-graph', figure={}),
            html.Br(),
            dcc.Graph(id='line-graph', figure={})
        ], width=8, align='start'),

        dbc.Col([
            html.Div(id='sales-table')
        ],width=4,style={'paddingLeft':'5%', 'paddingTop':'1%'})
    ]),
])


def Monthly_Sales():
    layout = html.Div([
        body
    ])
    return layout

'''
@app.callback(Output('pie-graph','figure'),
              [Input('year-dropdown','value'),
              Input('category-dropdown','value')])
def update_sales_graph_year(year_val, cat_val):
    df_monthly_sales = sales_utility.get_year_wise_sales(year_val, cat_val)
    return {'data':[
          go.Pie(
              labels=df_monthly_sales['month'],
              values=df_monthly_sales['SALE AMT.'],
              hole=.3
              )
          ],
          'layout': go.Layout(title='Sales Graph', margin={'b':0}, showlegend=False)}
'''

@app.callback(Output('pie-graph','figure'),
              [Input('year-dropdown','value'),
              Input('category-dropdown','value')])
def update_sales_graph_year(year_val, cat_val):
    df_monthly_sales = sales_utility.get_year_wise_sales(year_val, cat_val)
    return {'data':[
          go.Pie(
              labels=df_monthly_sales['month'],
              values=df_monthly_sales['SALE AMT.'],
              hole=.3
              )
          ],
          'layout': go.Layout(title='Sales Graph', margin={'b':0}, showlegend=False)}
#---------------------------------------------------------------------
@app.callback(Output('line-graph','figure'),
             [Input('year-dropdown','value'),
             Input('category-dropdown','value')])
def update_line_graph(year_val, cat_val):
    df_monthly_sales = sales_utility.get_year_wise_sales(year_val, cat_val)
    return {'data':[
        go.Scatter(x=df_monthly_sales['month'],
                   y=df_monthly_sales[df_monthly_sales['year']==yr]['SALE AMT.'],
                   mode='lines',
                   name=str(yr)) for yr in df_monthly_sales['year'].unique()
        ],
         'layout': go.Layout(margin={'t':0})}


@app.callback(Output('sales-table','children'),
             [Input('year-dropdown','value'),
             Input('category-dropdown','value')])
def update_sales_table(year_val, cat_val):
    final_df = sales_utility.get_year_wise_sales(year_val, cat_val).tail(12)
    return html.Div([
        dash_table.DataTable(
            id='sales_table',
            columns=[{"name": i, "id": i} for i in final_df.columns],
            data=final_df.to_dict("rows"),
            style_table={'width': '30%', 'paddingLeft':'10%',
                        'paddingTop':'5%', 'display':'inline-block'},
            style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left',

            } for c in ['year']
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

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Monthly_Sales()

if __name__ == "__main__":
    app.run_server()
