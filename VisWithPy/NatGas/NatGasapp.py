import dash
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__, use_pages=True)

pages = ["Home","Natural Gas Storage", "Natural Gas Production"]

app.layout = html.Div([
    html.Div(
	    html.H1(children='Natural Gas Analytics', className="header-title"),
        className="page-top"
    ),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    pages[0], href="/", className="nav-link"
                ),
                className="nav-bar"
            ),
            html.Div(
                dcc.Link(
                    pages[1], href="/natgasstorage", className="nav-link"
                ),
                className="nav-bar"
            ),
            html.Div(
                dcc.Link(
                    pages[2], href="/natgasproduction", className="nav-link"
                ),
                className="nav-bar"
            ),
        ], 
        className="nav-top"
    ),
	dash.page_container
] )

if __name__ == '__main__':
	app.run_server(host= '0.0.0.0',debug=True)