import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output
from tabs.boy.boy_top_list import Boy_Top_List
from tabs.boy.boy_brand import Boy_Brand
from tabs.boy.all_items import Boy_All_Items
from tabs.boy.boy_index import Boy_Index
from maindash import app

#app = dash.Dash(__name__)

layout = html.Div([
    dcc.Tabs(id="tabs-boy-props", value='tab-1', children=[
        dcc.Tab(label='Top List', value='top-list-tab'),
        dcc.Tab(label='Items', value='graphs-tab'),
        dcc.Tab(label='Brand', value='brand-tab'),
    ], colors={
        "border": "white",
        "primary": "gold",
        "background": "cornsilk"
    }),
    html.Div(id='boy-content-props')
])

def Boy_Layout():
    return layout

@app.callback(Output('boy-content-props', 'children'),
              [Input('tabs-boy-props', 'value')])
def render_content(tab):
    if tab == 'top-list-tab':
        return Boy_Top_List()
    elif tab == 'graphs-tab':
        return Boy_All_Items()
    elif tab == 'brand-tab':
        return Boy_Brand()
    else:
        return Boy_Index()
