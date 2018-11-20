import dash, dash_html_components as html, dash_core_components as dcc
from dash.dependencies import Input, Output
import math, pandas as pd

df = pd.read_csv("wfa_girls.txt", delimiter="\t")

app = dash.Dash(__name__)

app.layout = html.Div(id="app", children=[
    html.Label(["Weight:", dcc.Input(id="weight", type="number", value=10)]),
    dcc.Graph(id="graph")
])

@app.callback(Output('graph', 'figure'), [Input('weight', 'value')])
def cb(weight):
    return {
        "data": [
            {"x": df.Age, "y": df.P5},
            {"x": df.Age, "y": df.P50},
            {"x": df.Age, "y": df.P95},
            {"x": [1000], "y": [weight], "mode": "markers",
                "marker": {"size": 20}}
        ],
        "layout": {
            "title": "Weight for Age for Girls",
            "xaxis": {"title": "Age in Days"},
            "yaxis": {"title": "Weight in kg"}
        }
    }

app.run_server(debug=True)
