from dash import html, dcc
import dash_bootstrap_components as dbc

# It's good practice to import dependencies from your own project last.
from scenes.dashboardcomponents.heatmap import heatmapgraph
from scenes.config.database_config import EVENT_GROUPS

# --- Layout Configuration Constants ---
# Defining layout parameters as constants makes the code cleaner and easier to modify.
# The ** operator will unpack these dictionaries into keyword arguments for dbc.Col.
SIDEBAR_COLUMN_CONFIG = {"lg": 3, "md": 12, "sm": 12}
MAIN_CONTENT_COLUMN_CONFIG = {"lg": 6, "md": 12, "sm": 12}


def _create_left_sidebar(player_options):
    """Creates the left sidebar component with player and event filters."""
    return dbc.Col(
        html.Div([
            html.H4("Pick A Player", className="sidebar-title"),
            dcc.Dropdown(
                id='player-dropdown',
                options=player_options,
                value=player_options[0]['value'] if player_options else None,
                placeholder="Select a player",
                className="sidebar-dropdown"
            ),
            html.Div("Select Filters:", className="sidebar-section-header"),
            html.Div([
                html.Label("Event Type", className="sidebar-label"),
                dcc.Dropdown(
                    id='event-group-dropdown',
                    options=[{'label': k, 'value': k} for k in EVENT_GROUPS.keys()],
                    value="Attacking",
                    clearable=False,
                    className="sidebar-dropdown"
                ),
            ], className="sidebar-section"),
            html.Div([
                html.Label("Match Filters", className="sidebar-label"),
                dcc.Checklist(
                    id='match-checklist',
                    options=[],
                    value=[],
                    className="sidebar-checklist"
                )
            ], className="sidebar-section"),
        ], className="modern-sidebar"),
        **SIDEBAR_COLUMN_CONFIG
    )


def _create_main_content():
    """Creates the main content area for the heatmap visualization."""
    return dbc.Col(
        html.Div(heatmapgraph(), className="heatmap-container"),
        **MAIN_CONTENT_COLUMN_CONFIG
    )


def _create_right_sidebar():
    """Creates the right sidebar component with instructions for interpretation."""
    return dbc.Col(
        html.Div([
            html.H4("How do I interpret these visuals?", className="sidebar-title"),
            html.Ol([
                html.Li([
                    html.Span("Event Groups: ", style={"fontWeight": "bold"}),
                    "Select from Attacking or Defensive to focus on specific player actions.",
                    # Sub-list for event examples provides better structure.
                    html.Div([
                        html.Div(["Attacking: ", html.Span("Pass, Shot, Dribble, Carry, Cross")], className="event-example"),
                        html.Div(["Defensive: ", html.Span("Duel, Interception, Block, Clearance")], className="event-example"),
                    ], className="event-example-container")
                ]),
                html.Li([
                    html.Span("Colour: ", style={"fontWeight": "bold"}),
                    "Each event group uses a distinct color for its heatmap (e.g., red for Attacking, blue for Defensive)."
                ]),
                html.Li([
                    html.Span("Heatmap Intensity: ", style={"fontWeight": "bold"}),
                    "Darker areas indicate a higher concentration of player actions."
                ]),
                html.Li([
                    html.Span("Special Markers: ", style={"fontWeight": "bold"}),
                    "Red stars highlight goals, while other symbols may indicate key events."
                ]),
                html.Li([
                    html.Span("Interpretation: ", style={"fontWeight": "bold"}),
                    "Use the heatmap to identify a player's zones of activity."
                ]),
            ], className="instruction-list"),
        ], className="modern-sidebar"),
        lg=3,
        # Uses Bootstrap's display utilities to hide this column on screens
        # smaller than 'large' (lg). This ensures a clean mobile-first experience.
        className="d-none d-lg-block"
    )


def layout(player_options):
    """
    Generates the main application layout using Dash Bootstrap Components.

    This function assembles the primary UI components: a left sidebar for controls,
    a central area for the main visualization, and a right sidebar for instructions.
    The layout is fully responsive and optimized for both desktop and mobile viewing.

    Args:
        player_options (list): A list of dictionaries for the player dropdown,
                               e.g., [{'label': 'Player Name', 'value': 'player_id'}].

    Returns:
        dbc.Container: The complete, fluid Dash layout component.
    """
    return dbc.Container(
        [
            # This main row holds all the content and uses Bootstrap's grid system
            # to manage the arrangement of its child columns.
            dbc.Row(
                [
                    # -- Component 1: Control Panel / Left Sidebar --
                    _create_left_sidebar(player_options),

                    # -- Component 2: Main Visualization --
                    _create_main_content(),

                    # -- Component 3: Instructional / Right Sidebar --
                    _create_right_sidebar(),
                ]
            )
        ],
        fluid=True,
    )
