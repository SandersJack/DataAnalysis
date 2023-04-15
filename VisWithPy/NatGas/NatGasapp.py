# Author: Jack Sanders
# Created: 13/04/23

import pandas as pd
from dash import Dash, dcc, html, Input, Output

data = (
    pd.read_csv("dataSets/NatStorage_Full.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)

countries = data['Country'].sort_values().unique()

ex_style = [
    {
       "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet", 
    }
]

app = Dash(__name__,external_stylesheets=ex_style)
app.title = "Natural Gas Analytics"

app.layout = html.Div(
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
                                {'label': _country, 'value': _country}
                                for _country in countries
                            ], 
                            value="EU", 
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
                        id="full-chart", 
                        config={"displayModeBar":False},
                    ),
                    className = "card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children = dcc.Graph(
                        id="in-out-chart", 
                        config={"displayModeBar":False},
                    ),
                    className = "card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children = dcc.Graph(
                        id="consumtion-chart", 
                        config={"displayModeBar":False},
                    ),
                    className = "card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    Output('full-chart', 'figure'),
    Output('in-out-chart', 'figure'),
    Output('consumtion-chart', 'figure'),
    Input('country-filter', 'value'),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)

def update_charts(_country,start_date, end_date):
    
    f_data = data.query(
        "Country == @_country"
        " and Date >= @start_date and Date <= @end_date"
    ),
    
    #f_data = pd.DataFrame(f_data)
    f_data = f_data[0]
    #f_data.loc[f_data["Withdrawal [GWh/d]"] == '-' ,"Withdrawal [GWh/d]"] = 0
    #f_data["Withdrawal [GWh/d]"] = pd.to_numeric(f_data["Withdrawal [GWh/d]"])
    
    full_chart_fig = {
        "data": [
            {
                "x": f_data["Date"],
                "y": f_data["Gas in storage [TWh]"],
                "type": "lines", 
                "hovertemplate": "%{y:.2f}TWh<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Fullness of Gas Storage",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"title": "Date","fixedrange": True},
            "yaxis": {"title": "Gas Storage [TWh]", "fixedrange": True},
            "colorway": ["#87CEEB"],
        },
    }
    
    inout_chart_fig = {
        "data": [
            {
                "x": f_data["Date"],
                "y": f_data["Withdrawal [GWh/d]"],
                "type": "lines", 
                "name": "Withdrawal",
                "hovertemplate": "%{y:.2f}GWh/d<extra></extra>",
            },
            {
                "x": f_data["Date"],
                "y": f_data["Injection [GWh/d]"],
                "type": "lines", 
                "name": "Injection",
                "hovertemplate": "%{y:.2f}GWh/d<extra></extra>",
            },
            {
                "x": f_data["Date"],
                "y": f_data["Withdrawal capacity [GWh/d]"],
                "type": "lines", 
                "name": "Withdrawal Capacity",
                "hovertemplate": "%{y:.2f}GWh/d<extra></extra>",
            },
            {
                "x": f_data["Date"],
                "y": f_data["Injection capacity [GWh/d]"],
                "type": "lines", 
                "name": "Injection Capacity",
                "hovertemplate": "%{y:.2f}GWh/d<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Injection/Withdrawal of Gas",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"title": "Date","fixedrange": True},
            "yaxis": {"title": "Gas Input/Output [GWh/d]", "fixedrange": True},
            "colorway": ["#FF0078","#17B897"],
        },
    }
    
    consumption_chart_fig = {
        "data": [
            {
                "x": f_data["Date"],
                "y": f_data["Consumption [Twh]"],
                "type": "lines", 
                "hovertemplate": "%{y:.2f}TWh<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Consumption of Natural Gas (annual)",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"title": "Date","fixedrange": True},
            "yaxis": {"title": "Gas Consumption [TWh]", "fixedrange": True},
            "colorway": ["#87CEEB"],
        },
    }
    
    return full_chart_fig,inout_chart_fig,consumption_chart_fig

if __name__ == "__main__":
    app.run_server(host= '0.0.0.0',debug=True)