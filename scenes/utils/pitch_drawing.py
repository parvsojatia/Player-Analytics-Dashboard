import plotly.graph_objects as go

def draw_pitch_vertical(fig):
    pitch_shapes = [
        dict(type="rect", x0=0, y0=0, x1=80, y1=120, line=dict(color="black")),
        dict(type="line", x0=0, y0=60, x1=80, y1=60, line=dict(color="black")),
        dict(type="rect", x0=18, y0=0, x1=62, y1=18, line=dict(color="black")),
        dict(type="rect", x0=18, y0=102, x1=62, y1=120, line=dict(color="black")),
        dict(type="rect", x0=30, y0=0, x1=50, y1=6, line=dict(color="black")),
        dict(type="rect", x0=30, y0=114, x1=50, y1=120, line=dict(color="black")),
        dict(
            type="circle",
            x0=40 - 9.15, y0=60 - 9.15,
            x1=40 + 9.15, y1=60 + 9.15,
            line=dict(color="black")
        )
    ]
    
    fig.update_layout(shapes=pitch_shapes)
    fig.add_trace(go.Scatter(
        x=[40, 40], y=[12, 108],
        mode='markers',
        marker=dict(color="black", size=4),
        hoverinfo='skip',
        showlegend=False
    ))
    return fig


