#from maindash import app
from maindash import server
import dash
import dash_bootstrap_components as dbc
#from main import first_layout
#from main import render_page_content
from dash.dependencies import Input, Output

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

#app.layout = first_layout()


#@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
#def render_page_layout(pathname):
#    return render_page_content(pathname)


if __name__ == "__main__":
    app.run_server(debug=True)
