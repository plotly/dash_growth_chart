import dash, dash_html_components as html, dash_core_components as dcc
from dash.dependencies import Input, Output
import math, pandas as pd

df = pd.read_csv("wfa_girls.txt", delimiter="\t")

app = dash.Dash(__name__)

app.layout = dcc.Graph(figure={
    "data": [
        {"x": df.Age, "y": df.P5},
        {"x": df.Age, "y": df.P50},
        {"x": df.Age, "y": df.P95}
    ],
    "layout": {
        "title": "Weight for Age for Girls",
        "xaxis": {"title": "Age in Days"},
        "yaxis": {"title": "Weight in kg"}
    }
})

app.run_server(debug=True)
