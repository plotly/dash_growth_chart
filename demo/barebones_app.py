import dash, dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.H1("Hi there!")

app.run_server(debug=True)
