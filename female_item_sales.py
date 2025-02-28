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

#app = dash.Dash()
#app.config.suppress_callback_exceptions = True

df = pd.read_csv('./data/final_report.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)
#df.set_index('DATE',inplace=True)
print(df.columns)

temp_df = df[(df['item_type']=='female')][['PRODUCT NAME','month','SALE AMT.','QTY.']]
male_sales_df = temp_df.groupby(['PRODUCT NAME','month'])[['SALE AMT.','QTY.']].sum().reset_index()
#print(male_sales_df.head())

traces = []
for product in male_sales_df['PRODUCT NAME'].unique():
    trace = go.Bar(x=df['month'].unique(),
                   y=male_sales_df[male_sales_df['PRODUCT NAME']==product]['SALE AMT.'],
                   name=str(product))
    traces.append(trace)



layout = html.Div([
        html.Div([
            html.Div([
                html.H3('Total Sales')
            ],style={'width':'48%',
                    'border':'2px black solid',
                    'display':'inline-block',
                    'height':'40px',
                    'textAlign':'center',
                    'lineHeight':'10px'}),
            html.Div([
                html.H3('Total QTY.')
            ],style={'width':'48%',
                     'border':'2px black solid',
                     'display':'inline-block',
                     'height':'40px',
                     'textAlign':'center',
                     'lineHeight':'10px'})
        ]),

        html.Div([
            html.Div(id='sales-output',
                     style={'width':'48%',
                    'border':'2px black solid',
                    'display':'inline-block',
                    'height':'40px',
                    'textAlign':'center',
                    'lineHeight':'40px'}),
            html.Div(id='qty-output',
                     style={'width':'48%',
                     'border':'2px black solid',
                     'display':'inline-block',
                     'height':'40px',
                     'textAlign':'center',
                     'lineHeight':'40px'})
        ]),

        html.Div([
            dcc.Graph(id='female-item-sales',
                        figure={'data':[
                                go.Scatter(x=male_sales_df['month'].unique(),
                                           y=male_sales_df[male_sales_df['PRODUCT NAME']==product]['SALE AMT.'],
                                           mode='markers',
                                           opacity=0.7,
                                           marker=dict(size=male_sales_df[male_sales_df['PRODUCT NAME']==product]['QTY.']/2),
                                           name=str(product)) for product in male_sales_df['PRODUCT NAME'].unique()
                                ],
                                'layout': go.Layout(title='Female ITEMS Sales', hovermode='closest')}),
            html.Div(id='output-div'),
            dcc.Graph(id='female-item-sales1',
                        figure={'data':traces,
                                'layout': go.Layout(title='Female ITEMS Sales', barmode='stack')})

        ])
])

#app.layout = layout

@app.callback(Output('sales-output','children'),
            [Input('female-item-sales','clickData')])
def callback_sales(hoverData):
    if hoverData is None:
        return 'nothing yet'
    else:
        temp_list = hoverData['points'][0]
        sales = temp_list['y']
        return sales

@app.callback(Output('qty-output', 'children'),
            [Input('female-item-sales','clickData')])
def callback_qty(hoverData):
    if hoverData is None:
        return 'nothing yet'
    else:
        temp_list = hoverData['points'][0]
        qty = temp_list['marker.size'] * 2
        return qty

if __name__ == '__main__':
    app.run_server(debug=True)
