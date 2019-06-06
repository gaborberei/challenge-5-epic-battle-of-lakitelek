
# coding: utf-8

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

marka_ido_df = pd.read_csv("marka_ido.csv")



app.layout = html.Div([
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
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

