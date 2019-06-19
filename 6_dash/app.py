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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

loaded_model = pickle.load(open(str(Path("../5_modelling/data/finalized_model.sav")), 'rb'))
col_names = ["hany_eves","hany_eves_2","MEGTETT","MEGTETT_2","KLÍMA","LÉGZSÁK",\
             "ALUFELNI","ASR","AUTOMATA","BI-XENON","BLUETOOTH","TELJESITMENY LOERO",\
             "audi","mercedes-benz","bmw","infiniti","jaguar","land_rover","porsche",\
             "lexus","maserati","Hibrid","Elektromos","Dízel","Benzin"]

marka_ido_df = pd.read_csv(str(Path("../5_dash_prepare/data/marka_ido.csv")))

app.layout = html.Div(children=[

	html.H1(children='Ábra'),

    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=marka_ido_df[marka_ido_df['MARKA'] == m]['eladasig_nap'],
                    y=marka_ido_df[marka_ido_df['MARKA'] == m]['piacon_nap'],
                    text= m,
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 10,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=m
                ) for m in marka_ido_df.MARKA
            ],
            'layout': go.Layout(
                xaxis={'title': 'Az eladásig eltelt átlagos idő (nap)'},
                yaxis={'title': 'A jelenleg elérhető autók átlagos piacon töltött ideje'},
                #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        },
        style = {'height': 800}
    ),

    html.H1(children='Árbecslés'),

    html.Div(children='''
        Az árbecsléshez add meg a következő adatokat!
    '''),

    html.H6(children='1. Hány éves az autó?'),
    dcc.Input(
    placeholder='Enter a value...',
    type='number',
    id="ev"
    ),

    html.H6(children='2. Hány kilométert tett meg?'),
    dcc.Input(
    placeholder='Enter a value...',
    type='number',
    id="km"
    ),

    html.H6(children='3. Klíma?'),
    dcc.RadioItems(
    options=[
        {'label': 'Igen', 'value': '1'},
        {'label': 'Nem', 'value': '0'}
    ],
    value='0',
    id="klima"
    ),

    html.H6(children='4. Légzsák?'),
    dcc.RadioItems(
    options=[
        {'label': 'Igen', 'value': '1'},
        {'label': 'Nem', 'value': '0'}
    ],
    value='0',
    id="legzsak"
    ),

    html.H6(children='5. Alufelni?'),
    dcc.RadioItems(
    options=[
        {'label': 'Igen', 'value': '1'},
        {'label': 'Nem', 'value': '0'}
    ],
    value='0',
    id="alufelni"
    ),

    html.H6(children='6. ASR?'),
    dcc.RadioItems(
    options=[
        {'label': 'Igen', 'value': '1'},
        {'label': 'Nem', 'value': '0'}
    ],
    value='0',
    id="asr"
    ),

    html.H6(children='7. Automata?'),
    dcc.RadioItems(
    options=[
        {'label': 'Igen', 'value': '1'},
        {'label': 'Nem', 'value': '0'}
    ],
    value='0',
    id="automata"
    ),

    html.H6(children='8. Bixenon?'),
    dcc.RadioItems(
    options=[
        {'label': 'Igen', 'value': '1'},
        {'label': 'Nem', 'value': '0'}
    ],
    value='0',
    id="bixenon"
    ),

    html.H6(children='9. Bluetooth?'),
    dcc.RadioItems(
    options=[
        {'label': 'Igen', 'value': '1'},
        {'label': 'Nem', 'value': '0'}
    ],
    value='0',
    id="bluetooth"
    ),

    html.H6(children='10. Hány lóerős az autó?'),
    dcc.Input(
    placeholder='Enter a value...',
    type='number',
    id="loero"
    ),

    html.H6(children='11. Milyen márkájú?'),
    dcc.Dropdown(
    options=[
        {'label': 'Audi', 'value': 'audi'},
        {'label': 'Mercedes', 'value': 'mercedes-benz'},
        {'label': 'BMW', 'value': 'bmw'},
        {'label': 'Infiniti', 'value': 'infiniti'},
        {'label': 'Jaguar', 'value': 'jaguar'},
        {'label': 'Land_Rover', 'value': 'land_rover'},
        {'label': 'Porsche', 'value': 'porsche'},
        {'label': 'Lexus', 'value': 'lexus'},
        {'label': 'Maserati', 'value': 'maserati'}
        #{'label': 'Egyéb', 'value': 'egyeb'}
    ],
    #value='audi',
    id="marka",
    multi=False
    ),

    html.H6(children='12. Üzemanyag típusa'),
    dcc.RadioItems(
    options=[
        {'label': 'Benzin', 'value': 'Benzin'},
        {'label': 'Diesel', 'value': 'Dízel'},
        {'label': 'Elektromos', 'value': 'Elektromos'},
        {'label': 'Hibrid', 'value': 'Hibrid'}
    ],
    #value='Benzin',
    id="uzemanyag"
    ),

    html.H6(id="titkos")
])

@app.callback(Output('titkos', 'children'), [Input('ev', 'value'), Input('km', 'value'), Input('klima', 'value'), Input('legzsak', 'value'),
Input('alufelni', 'value'), Input('asr', 'value'), Input('automata', 'value'), Input('bixenon', 'value'), Input('bluetooth', 'value'), Input('loero', 'value'),
Input('marka', 'value'), Input('uzemanyag', 'value')])
def titok(ev, km, klima, legzsak, alufelni, asr, automata, bixenon, bluetooth, loero, marka, uzemanyag):
    d={'hany_eves': [ev], 'MEGTETT': [km], 'KLÍMA': [klima], 'LÉGZSÁK': [legzsak], 'ALUFELNI': [alufelni], 'ASR': [asr],
    'AUTOMATA': [automata], 'BI-XENON': [bixenon], 'BLUETOOTH': [bluetooth], 'TELJESITMENY LOERO': [loero], 'Márka': [marka],
    'Üzemanyag': [uzemanyag]}


    df = pd.DataFrame(data=d)


    df = df.join(pd.get_dummies(df["Márka"]))
    df = df.drop(["Márka"], axis = 1)

    df = df.join(pd.get_dummies(df["Üzemanyag"]))
    df = df.drop(["Üzemanyag"], axis = 1)

    df = df.applymap(int)

   # df["hany_eves_2"] = df["hany_eves"] ** 2
    #df["MEGTETT_2"] = df["MEGTETT"] ** 2

    #df.to_csv("proba_2.csv")

    print(df)

    df_final = pd.merge(pd.DataFrame(0,index=range(1),columns=col_names), df, how = "right",on = list(df.columns)).fillna(0)

    auto_erteke = 10 ** loaded_model.predict(df_final)[0]


    print(auto_erteke)
    return "az általad megadott auto értéke: " + str(int(auto_erteke)) + " Ft"

if __name__ == '__main__':
    app.run_server(debug=True)

#def update_output_div(input_value):
    #return 'You\'ve entered "{}"'.format(input_value)
