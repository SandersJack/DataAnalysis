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

data_price = (
    pd.read_csv("dataSets/NG_PRI_SUM_DCU_NUS_M.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%d/%m/%Y"))
    .sort_values(by="Date")
)

data_export = (
    pd.read_csv("dataSets/NG_MOVE_EXPC_S1_M.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%d/%m/%Y"))
    .sort_values(by="Date")
)

can_data_prod = (
    pd.read_csv("dataSets/canada-production.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%m/%d/%Y"))
    .sort_values(by="Date")
)

can_data_export = (
    pd.read_csv("dataSets/canada-import-export.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%d/%m/%Y"))
    .sort_values(by="Date")
)

can_data_LNG_export = (
    pd.read_csv("dataSets/canada-LNG-exports.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%d/%m/%Y"))
    .sort_values(by="Date")
)

can_data_LNG_export = can_data_LNG_export.loc[(can_data_LNG_export['Flow'] == "Exports") & (can_data_LNG_export['Terminal'] == "Total")]
can_data_export = can_data_export.loc[(can_data_export['Flow'] == "Exports") & (can_data_export['Region'] == "Total")]

Russia_data = (
    pd.read_csv("dataSets/russia-NatGas.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%m/%d/%Y"))
    .sort_values(by="Date")
)

prod_Russia_data = Russia_data.loc[(Russia_data['Type'] == "Production")][["Date","Million Standard Cubic Metres"]]
prod_Russia_data["MMCF"] = prod_Russia_data["Million Standard Cubic Metres"]*(1e6/28316.846592)

LNG_Russia_data= Russia_data.loc[(Russia_data['Type'] == "LNG")][["Date","Million Standard Cubic Metres"]]
LNG_Russia_data["MMCF"] = LNG_Russia_data["Million Standard Cubic Metres"]*(1e6/28316.846592)

pipe_Russia_data = Russia_data.loc[(Russia_data['Type'] == "Pipeline")][["Date","Million Standard Cubic Metres"]]
pipe_Russia_data["MMCF"] = pipe_Russia_data["Million Standard Cubic Metres"]*(1e6/28316.846592)


other_data = {"Russia": [prod_Russia_data,LNG_Russia_data,pipe_Russia_data]}

countries = ["United States", "Canada", "Russia"]

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
                    children="Production Data",
                    className="sub-header-title"
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
        html.Div(
            children=[
                html.Div(
                    children = dcc.Graph(
                        id="Export-chart", 
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
                        id="Price-chart", 
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
    Output('Export-chart', 'figure'),
    Output('Price-chart', 'figure'),
    Input('country-filter', 'value'),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)

def update_charts(_country,start_date, end_date):
    
    if(_country == "United States"):
    
        full_chart_fig = {
            "data": [
                {
                    "x": data["Date"],
                    "y": data["U.S. Natural Gas Gross Withdrawals (MMcf)"],
                    "type": "lines", 
                    "hovertemplate": "%{x:%m-%Y}<extra></extra>",
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
        
        export_chart_fig = {
            "data": [
                {
                    "x": data_export["Date"],
                    "y": data_export["Liquefied U.S. Natural Gas Exports (MMcf)"],
                    "type": "lines", 
                    "name": "Liquefied Exports",
                    "hovertemplate": "%{x:%m-%Y}<extra></extra>",
                },
                {
                    "x": data_export["Date"],
                    "y": data_export["U.S. Natural Gas Pipeline Exports (MMcf)"],
                    "type": "lines", 
                    "name": "Pipeline Exports",
                    "hovertemplate": "%{x:%m-%Y}<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": "Natural Gas Exports",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"title": "Date","fixedrange": True},
                "yaxis": {"title": "Gas Gross Withdrawals [MMcf]", "fixedrange": True},
                "colorway": ["#A020F0","#71797E"],
            },
        }
        
        price_chart_fig = {
            "data": [
                {
                    "x": data_price["Date"],
                    "y": data_price["Price of Liquefied U.S. Natural Gas Exports (Dollars per Thousand Cubic Feet)"],
                    "type": "lines", 
                    "name": "Liquefied Exports",
                    "hovertemplate": "%{x:%m-%Y}<extra></extra>",
                },
                {
                    "x": data_price["Date"],
                    "y": data_price["Price of U.S. Natural Gas Pipeline Exports (Dollars per Thousand Cubic Feet)"],
                    "type": "lines", 
                    "name": "Pipeline Exports",
                    "hovertemplate": "%{x:%m-%Y}<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": "Natural Gas Price",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"title": "Date","fixedrange": True},
                "yaxis": {"title": "Natural Gas Price [$/kCF]", "fixedrange": True},
                "colorway": ["#A020F0","#71797E"],
            },
        }
    
    elif(_country == "Canada"):
        full_chart_fig = {
            "data": [
                {
                    "x": can_data_prod["Date"],
                    "y": can_data_prod["Total (mmcf/d)"]*30.437,
                    "type": "lines", 
                    "hovertemplate": "%{x:%m-%Y}<extra></extra>",
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
        
        export_chart_fig = {
            "data": [
                {
                    "x": can_data_export["Date"],
                    "y": can_data_export["Volume (MCF)"],
                    "type": "lines", 
                    "name": "Exports",
                    "hovertemplate": "%{x:%m-%Y}<extra></extra>",
                },
                {
                    "x": can_data_LNG_export["Date"],
                    "y": can_data_LNG_export["Volume (MCF)"],
                    "type": "lines", 
                    "name": "LNG Exports",
                    "hovertemplate": "%{x:%m-%Y}<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": "Natural Gas Exports",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"title": "Date","fixedrange": True},
                "yaxis": {"title": "Gas Gross Withdrawals [Mcf]", "fixedrange": True},
                "colorway": ["#A020F0","#71797E"],
            },
        }
        
        price_chart_fig = {
            "data": [
                {
                    "x": can_data_export["Date"],
                    "y": can_data_export["Price (US$/kCF)"],
                    "type": "lines", 
                    "name": "Exports",
                    "hovertemplate": "%{x:%m-%Y}<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": "Natural Gas Price",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"title": "Date","fixedrange": True},
                "yaxis": {"title": "Natural Gas Price [$/kCF]", "fixedrange": True},
                "colorway": ["#A020F0","#71797E"],
            },
        }
    
    else:
        ch_data = other_data[_country]
        full_chart_fig = {
            "data": [
                {
                    "x": ch_data[0]["Date"],
                    "y": ch_data[0]["MMCF"],
                    "type": "lines", 
                    "hovertemplate": "%{x:%m-%Y}<extra></extra>",
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
        
        export_chart_fig = {
            "data": [
                {
                    "x": ch_data[1]["Date"],
                    "y": ch_data[1]["MMCF"],
                    "type": "lines", 
                    "name": "Pipeline Exports",
                    "hovertemplate": "%{x:%m-%Y}<extra></extra>",
                },
                {
                    "x": ch_data[2]["Date"],
                    "y": ch_data[2]["MMCF"],
                    "type": "lines", 
                    "name": "LNG Exports",
                    "hovertemplate": "%{x:%m-%Y}<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": "Natural Gas Exports",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"title": "Date","fixedrange": True},
                "yaxis": {"title": "Gas Gross Withdrawals [Mcf]", "fixedrange": True},
                "colorway": ["#A020F0","#71797E"],
            },
        }
        
        price_chart_fig = {
            "data": [
            ],
            "layout": {
                "title": {
                    "text": "Natural Gas Price",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"title": "Date","fixedrange": True},
                "yaxis": {"title": "Natural Gas Price [$/kCF]", "fixedrange": True},
                "colorway": ["#A020F0","#71797E"],
            },
        }

    
    return full_chart_fig,export_chart_fig, price_chart_fig

#if __name__ == "__main__":
#    app.run_server(host= '0.0.0.0',debug=True)