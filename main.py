import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Input, Output

from Analyzers.TrendAnalyzer import TrendAnalyzer
from Graph.Graph import Graph

app = Dash(__name__)

graph = Graph("BTCUSDT", "1h")
graph.load()

graph.add_analyzer(TrendAnalyzer(14, 2))
graph.start_analyze()

app.layout = html.Div(children=[
    dcc.Interval(id='graphsInterval', interval=1000, n_intervals=0),
    html.Div("", id="price"),
    dcc.Graph(
        id='graph',
        figure=graph.get_figure(),

    )
])


@app.callback(
    Output('graph', 'figure'),
    Input('graphsInterval', "n_intervals")
)
def update_graph(_):
    fig = graph.get_figure()
    return fig


@app.callback(
    Output('price', 'children'),
    Input('graphsInterval', "n_intervals")
)
def update_price(_):

    return graph.get_actual_price()


if __name__ == '__main__':
    app.run_server(debug=True)
