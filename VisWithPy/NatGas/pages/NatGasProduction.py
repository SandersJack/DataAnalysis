# Author: Jack Sanders
# Created: 13/04/23

import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, callback

dash.register_page(__name__)

data = (
    pd.read_csv("dataSets/NG_PROD_SUM_A_EPG0_FGW_MMCF_M.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%d/%m/%Y"))
    .sort_values(by="Date")
)

countries = ["United States"]

ex_style = [
    {
       "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet", 
    }
]

#app = Dash(__name__,external_stylesheets=ex_style)
#app.title = "Natural Gas Analytics"

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Natural Gas Analytics",
                    className="header-title"
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Country", className="menu-title"),
                        dcc.Dropdown(
                            id="country-filter",
                            options=[
                                {'label': html.Span( [
                                    #html.Img(src="/assets/imgs/flagicons/{}.png".format(_country), height=20),
                                    html.Span(_country,style={'font-size': 15, 'padding-left': 10}),
                                ],
                                ), 'value': _country}
                                for _country in countries
                                ],
                            value="United States", 
                            clearable=False, 
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children='Date Range', className='menu-title'
                        ),
                        dcc.DatePickerRange(
                            id='date-range',
                            min_date_allowed=data['Date'].min().date(),
                            max_date_allowed=data['Date'].max().date(),
                            start_date=data['Date'].min().date(),
                            end_date=data['Date'].max().date(),
                        ),
                    ]
                ),
            ],
            className="menu"
        ), 
        html.Div(
            children=[
                html.Div(
                    children = dcc.Graph(
                        id="Withdrawl-chart", 
                        config={"displayModeBar":False},
                    ),
                    className = "card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

@callback(
    Output('Withdrawl-chart', 'figure'),
    Input('country-filter', 'value'),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)

def update_charts(_country,start_date, end_date):
    
    full_chart_fig = {
        "data": [
            {
                "x": data["Date"],
                "y": data["U.S. Natural Gas Gross Withdrawals (MMcf)"],
                "type": "lines", 
                "hovertemplate": "%{y:.2f}MMcf<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Natural Gas Gross Withdrawals",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"title": "Date","fixedrange": True},
            "yaxis": {"title": "Gas Gross Withdrawals [MMcf]", "fixedrange": True},
            "colorway": ["#87CEEB"],
        },
    }
    

    
    return full_chart_fig

#if __name__ == "__main__":
#    app.run_server(host= '0.0.0.0',debug=True)