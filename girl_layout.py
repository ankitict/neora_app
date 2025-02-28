import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from tabs.girl.girl_top_list import Girl_Top_List
from tabs.girl.girl_brand import Girl_Brand
from tabs.girl.all_items import Girl_All_Items
from tabs.girl.girl_index import Girl_Index
from maindash import app


layout = html.Div([
    dcc.Tabs(id="tabs-girl-props", value='tab-1', children=[
        dcc.Tab(label='Top List', value='top-list-tab'),
        dcc.Tab(label='Items', value='graphs-tab'),
        dcc.Tab(label='Brand', value='brand-tab'),
    ], colors={
        "border": "white",
        "primary": "gold",
        "background": "cornsilk"
    }),
    html.Div(id='girl-content-props')
])

def Girl_Layout():
    return layout

@app.callback(Output('girl-content-props', 'children'),
              [Input('tabs-girl-props', 'value')])
def render_content(tab):
    if tab == 'top-list-tab':
        return Girl_Top_List()
    elif tab == 'graphs-tab':
        return Girl_All_Items()
    elif tab == 'brand-tab':
        return Girl_Brand()
    else:
        return Girl_Index()
