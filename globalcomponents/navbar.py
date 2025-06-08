
import dash_bootstrap_components as dbc
from dash import html

def get_navbar(pathname):
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(
                [html.I(className="fas fa-home me-2"), "Home"],
                href="/",
                className="nav-link",
                active=pathname == "/"
            )),
            dbc.NavItem(dbc.NavLink(
                [html.I(className="fas fa-chart-bar me-2"), "Dashboard"],
                href="/dashboard",
                className="nav-link",
                active=pathname == "/dashboard"
            )),
        ],
        brand=html.Div([
            html.I(className="fas fa-futbol me-2"),
            "Player Analytics Dashboard"
        ], className="navbar-brand"),
        color="dark",
        dark=True,
        className="navbar-custom mb-4",
        fluid=True
    )
