from maindash import app
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import base64
import datetime
import io
import pandas as pd
import os
from urllib.parse import quote as urlquote
import glob
from database import transforms
import dash

UPLOAD_DIRECTORY = "./data/upload_files"

#suppress_callback_exceptions=False
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

global combine

body = dbc.Container(
[
        dbc.Row(dbc.Col(html.H4('Upload your reports here')), align='center'),
        dbc.Row(
            dbc.Col(
                dcc.Upload(
                    id='file-upload',
                    children= html.Div([
                        'Drag and Drop or ', html.A('Select Files')
                    ]),
                    style={
                        'width':'100%',
                        'height':'60px',
                        'lineHeight':'60px',
                        'borderWidth':'1px',
                        'borderStyle':'dashed',
                        'borderRadius':'5px',
                        'textAlign':'center',
                        'margin':'10px'
                    },
                    multiple=True
                )
            )
        ),
        dbc.Row(
            dbc.Col([
                html.Div(id='output-data-upload'),
                html.Br(),
                html.Div(id='file-remove-id'),
            ])
        )
])

def File_upload():
    layout = html.Div([
        body
    ])
    return layout

def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

@app.callback(
    Output("output-data-upload", "children"),
    [Input("file-upload", "filename"), Input("file-upload", "contents")])
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""
    print('Callback Entered.....@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)
    files = uploaded_files()
    if len(files) == 0:
        lst = [html.Li("No files yet!")]
    else:
        df = transforms.get_files_data()
        df.to_csv('./data/final_report.csv')
        lst = [html.Li([filename, html.Button('Remove', id=filename.split('.')[0])])  for filename in files]
    return lst
    #else:
    #    return [html.Li(file_download_link(filename)) for filename in files]

temp_files = uploaded_files()

@app.callback(
    Output('file-remove-id', 'children'),
    [Input(name1.split('.')[0], 'n_clicks') for name1 in temp_files]
)
def remove_files(*button_clicks):
     ctx = dash.callback_context
     button_id = dash.callback_context.triggered[0]
     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
     if button_id['value']!=None:
         file_name = button_id["prop_id"].split(".")[0] + '.xls'
         os.remove(UPLOAD_DIRECTORY +'/'+ file_name)
         return 'File removed.. : ', file_name


#app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
#app.layout = File_upload()
