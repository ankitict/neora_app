import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output
from tabs.male.male_brand import Male_Brand
from tabs.male.male_top_list import Male_Top_List
from tabs.male.all_items_2 import All_Items
from tabs.male.male_index import Male_Index
from maindash import app

#app = dash.Dash(__name__)

layout = html.Div([
    dcc.Tabs(id="tabs-styled-with-props", value='tab-1', children=[
        dcc.Tab(label='Top List', value='top-list-tab'),
        dcc.Tab(label='Items', value='graphs-tab'),
        dcc.Tab(label='Brands', value='data-tab')
    ], colors={
        "border": "white",
        "primary": "gold",
        "background": "cornsilk"
    }),
    html.Div(id='tabs-content-props')
])

def Male_Layout():
    return layout

@app.callback(Output('tabs-content-props', 'children'),
              [Input('tabs-styled-with-props', 'value')])
def render_content(tab):
    if tab == 'top-list-tab':
        return Male_Top_List()
    elif tab == 'graphs-tab':
        return All_Items()
    elif tab == 'data-tab':
        return Male_Brand()
    else:
        return Male_Index()
