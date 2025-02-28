from maindash import server
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from file_upload import File_upload
from monthly_sales import Monthly_Sales
from female_layout import Female_Layout
from male_layout import Male_Layout
from boy_layout import Boy_Layout
from girl_layout import Girl_Layout
import dash_auth
from maindash import app
from maindash import server


#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#app.config.suppress_callback_exceptions = True

#app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
#server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "16rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("NEORA", className="display-4"),
        html.P(
            "The Innerjoy Lingerie Hub", className="lead"
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Upload", href="/upload", id="page-1-link"),
                html.Div('-----------------------------'),
                dbc.NavLink("Sales", href="/monthly_sales", id="page-2-link"),
                html.Div('-----------------------------'),
                dbc.NavLink("Male", href="/male_item_sales", id="page-3-link"),
                html.Div('-----------------------------'),
                dbc.NavLink("Female", href="/female_item_sales", id="page-4-link"),
                html.Div('-----------------------------'),
                dbc.NavLink("Boy", href="/boy_item_sales", id="page-5-link"),
                html.Div('-----------------------------'),
                dbc.NavLink("Girl", href="/girl_item_sales", id="page-6-link"),
                html.Div('-----------------------------'),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

#layout = html.Div([dcc.Location(id="url"), sidebar, content])

#def first_layout():
#    return layout

app.layout = html.Div([dcc.Location(id="url", refresh=False), sidebar, content])

@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 5)]

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/","/upload"]:
        return File_upload()
    elif pathname == "/monthly_sales":
        return Monthly_Sales()
    elif pathname == "/male_item_sales":
        return Male_Layout()
    elif pathname == "/female_item_sales":
        return Female_Layout()
    elif pathname == "/boy_item_sales":
        return Boy_Layout()
    elif pathname == "/girl_item_sales":
        return Girl_Layout()
    # If the user tries to reach a different page, return a 404 message
    #df = sales_utility.get_df()
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=False)
