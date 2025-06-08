from dash import dcc
import plotly.graph_objects as go

def empty_placeholder_figure():
    fig = go.Figure()
    fig.update_layout(
        title="Please select a player and matches",
        plot_bgcolor='white',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=600
    )
    return fig


def heatmapgraph():
    return dcc.Loading(
        id='loading-graph',
        type='circle',
        children=[
            dcc.Graph(
                id='heatmap-graph',
                figure=empty_placeholder_figure(),  # << preload default
                config={
                    'displayModeBar': True,   
                    'editable': False,
                    'staticPlot': False,
                    'displaylogo': False
                },
                style={'height': '100vh', 'width': '100%', 'padding': '0px'}

            )
        ]
    )
