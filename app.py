import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import os
from scenes.config.database_config import engine
from globalcomponents.navbar import get_navbar
from scenes.database.data_loader import load_players, load_player_matches
from scenes.utils.kde_calculation import compute_kde
from scenes.utils.heatmap_creation import create_vertical_heatmap
from scenes.pages import dashboard, home

# ------------------------------------------------------------------------------
# 🔧 App Initialization
# ------------------------------------------------------------------------------
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

server = app.server 

app.title = "Player Analytics Dashboard"

# ------------------------------------------------------------------------------
# 🚀 Load player list once at app startup
# ------------------------------------------------------------------------------
try:
    player_options = load_players(engine)
except Exception as e:
    print(f"[Startup Error] Failed to load player options: {e}")
    player_options = []

# ------------------------------------------------------------------------------
# 📄 App Layout
# ------------------------------------------------------------------------------
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='navbar-container'),
    html.Div(id='page-content')
])

@app.callback(
    Output('navbar-container', 'children'),
    Input('url', 'pathname')
)
def update_navbar(pathname):
    return get_navbar(pathname)

# ------------------------------------------------------------------------------
# 🔁 Page Routing Callback
# ------------------------------------------------------------------------------
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    """Handles routing between pages."""
    if pathname == '/dashboard':
        return dashboard.layout(player_options)
    return home.layout()

# ------------------------------------------------------------------------------
# 🔁 Match Checklist Update on Player Select
# ------------------------------------------------------------------------------
@app.callback(
    [Output('match-checklist', 'options'),
     Output('match-checklist', 'value')],
    Input('player-dropdown', 'value')
)
def update_match_options(player_id):
    """Fetches match options for the selected player."""
    if player_id is None:
        return [], []
    
    try:
        options = load_player_matches(player_id, engine)
        values = [opt['value'] for opt in options]
        return options, values
    except Exception as e:
        print(f"[Callback Error] Match loading failed: {e}")
        return [], []

# ------------------------------------------------------------------------------
# 🔁 Heatmap Update on Player / Match / Group Change
# ------------------------------------------------------------------------------
@app.callback(
    Output('heatmap-graph', 'figure'),
    [
        Input('player-dropdown', 'value'),
        Input('match-checklist', 'value'),
        Input('event-group-dropdown', 'value')
    ]
)
def update_heatmap(player_id, selected_matches, selected_group):
    """Generates updated heatmap based on user input."""
    if not player_id or not selected_matches:
        # Use a placeholder name if no player is selected
        return create_vertical_heatmap(None, selected_group or "Attacking", "No player selected")

    # Find player name from player_id using player_options
    player_name = next(
        (p['label'] for p in player_options if p['value'] == player_id),
        "Unknown Player"
    )

    try:
        kde_data = compute_kde(
            player_id=player_id,
            match_ids=selected_matches,
            group=selected_group
        )
        return create_vertical_heatmap(kde_data, selected_group, player_name)
    except Exception as e:
        print(f"[Callback Error] Heatmap rendering failed: {e}")
        return create_vertical_heatmap(None, selected_group, player_name)

# ------------------------------------------------------------------------------
# 🏁 Run Server
# ------------------------------------------------------------------------------
if __name__ == '__main__':
   app.run(debug=False, host='0.0.0.0', port=5432)
