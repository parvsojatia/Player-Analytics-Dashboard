from dash import html
import dash_bootstrap_components as dbc

def layout():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    [
                        html.H2("About this App", className="mt-4 mb-3"),
                        html.Hr(),

                        # Motivation Section
                        html.H5("Motivation", className="mt-4 mb-2"),
                        html.P(
                            "Driven by a deep curiosity for both football and data analytics, I embarked on this project to explore how data-driven insights can enhance our understanding of the beautiful game. By combining my passion for football with my interest in analytical methods, I aim to uncover meaningful patterns and provide new perspectives on player performance and match dynamics using modern data science techniques.",
                            className="mb-3"
                        ),

                        # About The Data Source Section
                        html.H5("About the Data Source", className="mt-4 mb-2"),
                        html.P(
                            "This dashboard utilizes StatsBomb's open World Cup 2022 dataset, which provides detailed event-level tracking for every match of the tournament. The data includes comprehensive spatial coordinates (x, y) for various event types including passes, shots, dribbles, defensive actions, and more. Each event contains rich metadata such as player information, timestamps, outcomes, and contextual details. The dataset has been processed and stored in a PostgreSQL database with optimized schema design for efficient querying and visualization. StatsBomb's data standard ensures consistent spatial mapping across all matches, enabling accurate cross-match comparisons.",
                            className="mb-3"
                        ),

                        # Upcoming Features Section
                        html.H5("Upcoming Features", className="mt-4 mb-2"),
                        dbc.Alert(
                            [
                                html.Ul([
                                    html.Li("Player Metrics Card: Display key player statistics in a visually appealing card format."),
                                    html.Li("UI Improvements: Enhance the dashboard's layout, colors, and interactivity for a better user experience."),
                                    html.Li("Radar Chart: Visualize player attributes and performance metrics using interactive radar (spider) charts."),
                                    html.Li("Player Comparison: Compare multiple players side-by-side across various metrics and visualizations."),
                                ])
                            ],
                            color="rgb(140, 205, 235)",
                            className="mb-4"
                        ),

                        # GitHub Code Section
                        html.H5("GitHub Code", className="mt-4 mb-2"),
                        html.P(
                            [
                                "Interested in looking at the code for this web-application? ",
                                html.A("Click here to view the source code!",
                                       href="https://github.com/parvsojatia/Player-Analytics-Dashboard",
                                       target="_blank",
                                       className="text-primary",
                                       style={"textDecoration": "none"})
                            ],
                            className="mb-3"
                        ),

                        # Developed By Section
                        html.H5("Developed By:", className="mt-4 mb-2"),
                        html.P(
                            "Parv Sojatia (Parvsojatia40@gmail.com)",
                            className="mb-4"
                        ),
                    ],
                    width=10, lg=8
                ),
                justify="center"
            )
        ],
        fluid=True
    )
