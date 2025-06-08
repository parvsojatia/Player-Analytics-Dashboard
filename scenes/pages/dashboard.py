from dash import html, dcc
import dash_bootstrap_components as dbc
from scenes.dashboardcomponents.heatmap import heatmapgraph
from scenes.config.database_config import EVENT_GROUPS

def layout(player_options):
    return dbc.Container([
        dbc.Row([

            # === LEFT SIDEBAR ===
            dbc.Col(
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
                width=3
            ),

            # === MAIN HEATMAP SECTION ===
            dbc.Col(
                html.Div(heatmapgraph(), className="heatmap-container"),
                width=6
            ),
            # === RIGHT SIDEBAR ===
            dbc.Col(
                html.Div([
                    html.H4("How do I interpret these visuals?", className="sidebar-title"),
                    html.Ol([
                        html.Li([
                            html.Span("Event Groups: ", style={"fontWeight": "bold"}),
                            "Select from Attacking or Defensive to focus on specific player actions.",
                            html.Div([
                                html.Div([
                                    html.Span("Attacking: ", style={"fontWeight": "bold"}),
                                    html.Span("Pass, Shot, Dribble, Carry, Cross", style={"marginLeft": "0.25rem"})
                                ], style={"marginTop": "0.5rem"}),
                                html.Div([
                                    html.Span("Defensive: ", style={"fontWeight": "bold"}),
                                    html.Span("Duel, Interception, Block, Clearance", style={"marginLeft": "0.25rem"})
                                ], style={"marginTop": "0.25rem"}),
                            ], style={"marginLeft": "1rem", "marginBottom": "0.5rem"})
                        ]),
                        html.Li([
                            html.Span("Colour: ", style={"fontWeight": "bold"}),
                            "Each event group uses a distinct color for its heatmap (e.g., red for Attacking, blue for Defensive)."
                        ]),
                        html.Li([
                            html.Span("Heatmap Intensity: ", style={"fontWeight": "bold"}),
                            "Darker or more intense areas indicate a higher concentration of player actions in those zones."
                        ]),
                        html.Li([
                            html.Span("Special Markers: ", style={"fontWeight": "bold"}),
                            "Red stars highlight goals, while other symbols may indicate missed shots or key events."
                        ]),
                        html.Li([
                            html.Span("Interpretation: ", style={"fontWeight": "bold"}),
                            "Use the heatmap to identify where on the pitch a player is most active for the selected event type."
                        ]),
                    ], className="instruction-list"),
                ], className="modern-sidebar"),
                width=3
            )


        ])
    ], fluid=True)
