import numpy as np
from io import BytesIO as _BytesIO
from PIL import Image
import base64

import flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from keras.models import load_model
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input

# some global variables
# CANDY_IDX   : current index of candy list, '10' means no candy selected
# MODEL       : CNN model on AWS server
# CANDY_LIST  : list of candy, should match the list in model training .py
# INGREDIENTS : list of allergens in candy 
CANDY_IDX = 10 
MODEL = load_model('model.h5')

CANDY_LIST = ['Kitkat','M&Ms Peanut','M&Ms Chocolate','M&Ms Peanut Butter',
        'Snicker','Snicker Peanut','Snicker Almond','Reese','Heath','Whoppers',
        'Try Again']

INGREDIENTS = [['milk','wheat','soy'],
               ['milk','soy','peanut'],
               ['milk','soy'],
               ['milk','soy','peanut'],
               ['milk','soy','peanut','egg'],
               ['milk','soy','peanut','egg'],
               ['milk','soy','almond','egg'],
               ['milk','peanut','soy'],
               ['milk','almond','soy'],
               ['milk','wheat','soy'],
               []]



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # title, with color letters
    html.H2(       
        html.Div([
            html.Span('S', style={'color': 'red'}),
            html.Span('u', style={'color': 'orange'}),
            html.Span('g', style={'color': 'gold'}),
            html.Span('a', style={'color': 'green'}),
            html.Span('r ', style={'color': 'blue'}),
            html.Span('F', style={'color': 'purple'}),
            html.Span('a', style={'color': 'red'}),
            html.Span('i', style={'color': 'orange'}),
            html.Span('r', style={'color': 'gold'}),
            html.Span('y', style={'color': 'green'}),  
        ]),
        style={
            'fontSize': 50, 
            'fontWeight': 'bold', 
            'textAlign': 'center'
        }
    ),


    # allergen check-box
    html.Div(
        dcc.Checklist(id='allergen',
            options=[
                {'label': 'Milk', 'value': 'milk'},
                {'label': 'Peanut', 'value': 'peanut'},
                {'label': 'Almond', 'value': 'almond'},
                {'label': 'Soy', 'value': 'soy'},
                {'label': 'Wheat', 'value': 'wheat'},
                {'label': 'Egg', 'value': 'egg'}
            ],
            value=[],
            labelStyle={'display': 'inline-block'},
            inputStyle={"margin-left": "10px"}  
        )
    ),
    html.H5(''),

    # upload file box
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            html.Span('Drag and Drop or ', style={'color': 'goldenrod'}), 
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '0px',
            'fontSize': 30,
            'font-weight': 'bold',
            'background-image': 'url("/assets/background.jpg")'
        }
    ),

    # image and check button, showed in 2 columns 
    html.Div([
        html.Div(id='output-image-upload', className='six columns'),

        html.Div([
            html.Hr(),
            html.Button(id='submit-button', n_clicks=0, children='Check', 
                style={'fontSize': 16, 'color': 'steelblue'}),

            html.Div(id='output-allergy',
                children='', style={'paddingTop': '10px'}),
            html.Hr()
            ], className='six columns', style={'align': 'center'})
    ], className='row')
])


def predict_img(contents):    
    # convert html object to pil image
    string = contents.split(';base64,')[-1]
    decoded = base64.b64decode(string)
    buff = _BytesIO(decoded)
    im = Image.open(buff)

    # resize image to 224x224 np array for input
    im = im.resize((224,224))
    img_array = np.asarray(im)
    img_array = np.expand_dims(img_array, axis=0)

    global CANDY_IDX

    # predict candy type, assign '10' if probability is less than 0.98
    pred = MODEL.predict(preprocess_input(img_array))

    if np.amax(pred)>0.98:
        CANDY_IDX = np.argmax(pred, axis=1)[0]
    else:
        CANDY_IDX = 10

    candy_name = CANDY_LIST[CANDY_IDX]

    return html.Div([
        html.Hr(),
        html.H5(candy_name),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents, width='224', height='224'),
        html.Hr()
    ])

@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents')])
def update_output(contents):
    if contents is not None:
        return predict_img(contents)    
        

@app.callback(Output('output-allergy', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('allergen', 'value')])
def update_output(n_clicks, a):
    if any(x in a for x in INGREDIENTS[CANDY_IDX]):
        return html.Div('ALLERGEN WARNING',
            style={
                'color': 'white',
                'fontSize': 20, 
                'fontWeight': 'bold',
                'backgroundColor': 'tomato',
                'width': '200px',
                'textAlign': 'center'})
    else:
        return html.Div('YUMMY', 
            style={
                'color': 'white',
                'fontSize': 20, 
                'fontWeight': 'bold',
                'backgroundColor': 'yellowgreen',
                'width': '200px',
                'textAlign': 'center'})

if __name__ == '__main__':
    app.run_server(debug=True)
