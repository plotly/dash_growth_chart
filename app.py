import dash, dash_html_components as html, dash_core_components as dcc
from dash.dependencies import Input, Output
import math, pandas as pd
from datetime import datetime as dt

weight_data = dict( boy=pd.read_csv("wfa_boys.txt", delimiter="\t"),
                    girl=pd.read_csv("wfa_girls.txt", delimiter="\t"))
height_data = dict( boy=pd.read_csv("lhfa_boys.txt", delimiter="\t"),
                    girl=pd.read_csv("lhfa_girls.txt", delimiter="\t"))

app = dash.Dash(__name__)

app.layout = html.Div(id="app", children=[
    dcc.RadioItems(id='sex', value='girl',
        options=[dict(label=x, value=x) for x in ['girl', 'boy']]),
    html.Label(children=["Height (cm):",
        dcc.Input(id='height', value=70, type="number", step=1)]),
    html.Label(children=["Weight (kg):",
        dcc.Input(id='weight', value=10, type="number", step=0.1)]),
    html.Label(children=["Born on:",
        dcc.DatePickerSingle(id="birthday", date=dt(2018, 1, 1)),]),
    html.H3(id='output'),
    dcc.Graph(id="height_chart"),
    dcc.Graph(id="weight_chart"),
])

def percentile(dataset, days, x):
    L,M,S = dataset[["L","M","S"]].values[int(days)]
    return int(50 * (math.erf((((x/M) ** L - 1)/(L*S)) /2**.5)+1))

@app.callback(Output('output', 'children'),
    [Input('sex', 'value'), Input('birthday', 'date'),
    Input('height', 'value'), Input('weight', 'value')])
def cb(sex, birthday, height, weight):
    days = (dt.now() - dt.strptime(birthday, '%Y-%m-%d')).days
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
    return "{} percentile for weight, {} percentile for height".format(
        ordinal(percentile(weight_data[sex], days, weight)),
        ordinal(percentile(height_data[sex], days, height)))

def curve(x, p5, p50, p95, child_x, child_y, y_label):
    data = [
        {"name": "Median", "x": x/30.0, "y": p50,
            "line": {"color": "#aaa"}},
        {"name": "5th percentile", "x": x/30.0, "y": p5,
            "line": {"color": "#ddd"}},
        {"name": "95th percentile", "x": x/30.0, "y": p95,
            "line": {"color": "#ddd"}, "fill": 'tonexty'},
        {"name": "Child", "x": [child_x/30.0], "y": [float(child_y)],
            "mode": "markers", "marker": {"symbol": "star", "size": 10}}
    ]
    layout = {
        "height": 300,
        "xaxis": {"title": "Age in months", "showline": True},
        "yaxis": {"title": y_label},
        "showlegend": False, "hovermode": "closest",
        "margin": {"t": 30, "b": 60, "l": 60, "r": 60},
        "annotations": [{ "text": y_label+ " for Age",
            "font": {"size": 18}, "x": 0.03, "y": 1,
            "xref": "paper", "yref": "paper", "showarrow": False }]
    }
    return {"data": data, "layout": layout}

@app.callback(Output('height_chart', 'figure'), [Input('sex', 'value'),
    Input('birthday', 'date'), Input('height', 'value')])
def cb(sex, birthday, height):
    days = (dt.now() - dt.strptime(birthday, '%Y-%m-%d')).days
    h = height_data[sex].head(days*2)
    return curve(h.Day, h.P5, h.P50, h.P95, days, height, "Length/Height")

@app.callback(Output('weight_chart', 'figure'), [Input('sex', 'value'),
    Input('birthday', 'date'), Input('weight', 'value')])
def cb(sex, birthday, weight):
    days = (dt.now() - dt.strptime(birthday, '%Y-%m-%d')).days
    w = weight_data[sex].head(days*2)
    return curve(w.Age, w.P5, w.P50, w.P95, days, weight, "Weight")

app.run_server(debug=True)
