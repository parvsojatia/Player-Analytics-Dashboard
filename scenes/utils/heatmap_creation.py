import plotly.graph_objects as go
from scenes.utils.pitch_drawing import draw_pitch_vertical
from scenes.config.database_config import COLOR_MAPPING

def create_vertical_heatmap(kde_result, group: str, player_name: str):
    """
    Creates a vertical football pitch heatmap using KDE results and Plotly.

    Parameters:
        kde_result (tuple or None): Output from the KDE function.
        group (str): The event group (e.g., 'Attacking', 'Defending').
        player_name (str): The selected player's name.

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly figure object with the heatmap.
    """
    if kde_result is None:
        return go.Figure().update_layout(title="No event data available")

    xi, yi, z, x, y, types, outcomes = kde_result
    fig = go.Figure()
    group_color = COLOR_MAPPING.get(group, '#636363')

    # Heatmap
    fig.add_trace(go.Contour(
        z=z, x=xi, y=yi,
        colorscale=[[0, 'white'], [1, group_color]],
        opacity=0.85,
        showscale=False,
        hoverinfo='skip',
        contours=dict(showlines=False),
        name=f'{group} Heatmap',
        showlegend=False
    ))

    # Background dots
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='markers',
        marker=dict(size=2, color='black', opacity=0.3),
        hoverinfo='skip',
        showlegend=False
    ))

    # Shots and goals
    shot_x_goal = [x[i] for i in range(len(types)) if types[i] == 'Shot' and outcomes[i] == 'Goal']
    shot_y_goal = [y[i] for i in range(len(types)) if types[i] == 'Shot' and outcomes[i] == 'Goal']
    shot_x_miss = [x[i] for i in range(len(types)) if types[i] == 'Shot' and outcomes[i] != 'Goal']
    shot_y_miss = [y[i] for i in range(len(types)) if types[i] == 'Shot' and outcomes[i] != 'Goal']

    if shot_x_miss:
        fig.add_trace(go.Scatter(
            x=shot_x_miss, y=shot_y_miss,
            mode='markers',
            marker=dict(size=10, color='black', symbol='circle', opacity=0.7),
            name='Shots'
        ))

    if shot_x_goal:
        fig.add_trace(go.Scatter(
            x=shot_x_goal, y=shot_y_goal,
            mode='markers',
            marker=dict(size=12, color='red', symbol='star', opacity=0.9),
            name='Goals'
        ))

    fig = draw_pitch_vertical(fig)

    # Add dynamic title
    fig.update_layout(
        title=f"{player_name} — {group} Event's Heatmap",
        autosize=True,
        margin=dict(l=10, r=10, t=50, b=10),  # t=50 for more title space
        plot_bgcolor='white',
        showlegend=True,
        xaxis=dict(showticklabels=False, scaleanchor="y", fixedrange=True, constrain='domain'),
        yaxis=dict(showticklabels=False, scaleanchor="x", fixedrange=True, constrain='domain')
    )

    return fig
