import dash, dash_html_components as html, dash_core_components as dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div(children = [
  dcc.Input(id="name", value="you"),
  html.H1(id="greeting", children=["Hi there!"])
])

@app.callback(Output('greeting', 'children'), [Input('name', 'value')])
def cb(name):
    return "Hi there, %s!" % name

app.run_server(debug=True)
