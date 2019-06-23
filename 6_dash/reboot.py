# coding=utf-8

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.plotly as py
import plotly.graph_objs as go
import pickle
import pandas as pd
from pathlib import Path
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                )
#app.config['suppress_callback_exceptions']=True

loaded_model = pickle.load(open(str(Path("../5_modelling/data/finalized_model.sav")), 'rb'))

marka_ido_df = pd.read_csv(str(Path("../5_dash_prepare/data/marka_ido.csv")))

with open('../5_modelling/data/dict.json') as json_file:  
    data_dict = json.load(json_file)

numbers = [val for idx,val in enumerate(data_dict["number"]) if data_dict["number"][idx][:5]!=data_dict["number"][idx-1][:5]]

col_names = numbers + data_dict["boolen"]+ list(data_dict["Dropdown"].keys())

def numbers_func(x):
    
    return html.Div([html.H6(children='Ennek a száma:' + x),dcc.Input(
    placeholder='Enter a value...',
    type='number',
    id=x
    )])

def boolen_func(x):
    
    return html.Div([html.H6(children='Van-e benne:' + x),dcc.RadioItems(
    options=[
        {'label': 'Igen', 'value': '1'},
        {'label': 'Nem', 'value': '0'}
    ],
    value='0',
    id=x
    )])

def dropdown_func(key):

    return  html.Div([html.H6(children='Válasz ezek közül egyet, vagy ha nem tudsz hagyd üresen!'),
    dcc.Dropdown(
    options=[ {'label':x,'value':x} for x in data_dict["Dropdown"][key]],

    id=key,
    multi=False
    )])


numbers_list = [numbers_func(i) for i in numbers]
boolen_list = [boolen_func(i) for i in data_dict["boolen"]]
dropdown_list = [ dropdown_func(key) for key in data_dict["Dropdown"].keys()]

app.layout = html.Div([html.Div(id='titkos')] + numbers_list + boolen_list + dropdown_list)

@app.callback(Output('titkos', 'children'),
[Input(x, 'value') for x in col_names])

#[Input(x, 'value') for x in col_names]
def titok(*arglist):
    d = {col_names[idx]:arglist[idx] for idx in range(12)}

    df = pd.DataFrame(data=d, index = [0])


    df = df.join(pd.get_dummies(df["auto_marka"]))
    df = df.drop(["auto_marka"], axis = 1)

    df = df.join(pd.get_dummies(df["hajtaslanc"]))
    df = df.drop(["hajtaslanc"], axis = 1)

    df = df.applymap(int)

    #df["hany_eves_2"] = df["hany_eves"] ** 2
    #df["MEGTETT_KM_2"] = df["MEGTETT_KM"] ** 2

    df_final = pd.merge(pd.DataFrame(0,index=range(1),columns=data_dict["all"]), df, how = "right",on = list(df.columns)).fillna(0)

    auto_erteke = 10 ** loaded_model.predict(df_final)[0]

    
    print(auto_erteke)
    return "az általad megadott auto értéke: " + str(int(auto_erteke)) + " Ft"

if __name__ == '__main__':
    app.run_server(debug=True)

#def update_output_div(input_value):
    #return 'You\'ve entered "{}"'.format(input_value)
