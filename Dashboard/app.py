from matplotlib.colors import LightSource
import dash
from dash import dcc, html, Output, Input, State
import dash_labs as dl
import dash_bootstrap_components as dbc
from pages import upload

app = dash.Dash(
    __name__, plugins=[dl.plugins.pages], suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.BOOTSTRAP]
)
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Upload", href="/upload"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)

offcanvas = html.Div(
    [
        dbc.Button("Menu", color="light", id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas(
            dbc.ListGroup(
                [
                    #dbc.ListGroupItem(dcc.Link('Home',href ="/Home")),
                    
                    
                    dbc.ListGroupItem(page["name"], href=page["path"])
                    for page in dash.page_registry.values()
                    if page["module"] != "pages.not_found_404"
                    
                ]
          
            ),
            id="offcanvas",
            is_open=False,
        ),
       
    ],
    className="my-3"
)

app.layout = html.Div([
    #navbar,
    dbc.Container([offcanvas, dl.plugins.page_container],
    fluid=True,
)])
 

@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True, port=5000)