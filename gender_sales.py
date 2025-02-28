import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from datetime import datetime
import numpy as np

app = dash.Dash()

df = pd.read_csv('./data/final_report.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)
#df.set_index('DATE',inplace=True)
print(df.columns)

item_wise_sales = df.groupby(['item_type','month'])[['SALE AMT.']].sum().reset_index()

app.layout = html.Div([
        html.Div([

            dcc.Graph(id='item-wise-sales',
                      figure={'data':[
                            go.Scatter(x=item_wise_sales['month'],
                                                y=item_wise_sales[item_wise_sales['item_type']==item]['SALE AMT.'],
                                                mode='markers',
                                                opacity=0.7,
                                                marker=dict(size=15),
                                                name=str(item)) for item in item_wise_sales['item_type'].unique()
                            ],
                            'layout': go.Layout(title='Gender wise Sales')}
                    ),

        dcc.Graph(id='item-wise-sales1',
                    figure={'data':[
                            go.Scatter(x=item_wise_sales['month'],
                                       y=item_wise_sales[item_wise_sales['item_type']==item]['SALE AMT.'],
                                       mode='lines+markers',
                                       opacity=0.7,
                                       marker=dict(size=10),
                                       name=str(item)) for item in item_wise_sales['item_type'].unique()
                            ],
                            'layout': go.Layout(title='Gender wise Sales')})
        ])
])

if __name__ == '__main__':
    app.run_server()
