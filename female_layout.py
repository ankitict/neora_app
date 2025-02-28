import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output
from tabs.female.female_top_list import Female_Top_List
from tabs.female.female_brand import Female_Brand
from tabs.female.all_items import Female_All_Items
from tabs.female.female_index import Female_Index
from maindash import app

#app = dash.Dash(__name__)

layout = html.Div([
    dcc.Tabs(id="tabs-female-props", value='tab-1', children=[
        dcc.Tab(label='Top List', value='top-list-tab'),
        dcc.Tab(label='Items', value='graphs-tab'),
        dcc.Tab(label='Brand', value='data-tab')
    ], colors={
        "border": "white",
        "primary": "gold",
        "background": "cornsilk"
    }),
    html.Div(id='female-content-props')
])

def Female_Layout():
    return layout

@app.callback(Output('female-content-props', 'children'),
              [Input('tabs-female-props', 'value')])
def render_content(tab):
    if tab == 'top-list-tab':
        return Female_Top_List()
    elif tab == 'graphs-tab':
        return Female_All_Items()
    elif tab == 'data-tab':
        return Female_Brand()
    else:
        return Female_Index()
