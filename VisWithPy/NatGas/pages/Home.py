import dash
from dash import html, dcc
import pandas as pd

dash.register_page(__name__, path='/')

cont_data = (
    pd.read_csv("dataSets/continent-data.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y"))
    .sort_values(by="Date")
)
continents = []

for col in cont_data.columns:
    if "exports" in col:
        continents.append(col[24:-8])

layout = html.Div(children=[
    html.Div(children=[
        html.H1(children='Welcome to this Dash-Board',className="sub-header-title"),
    ], className="home-sub-title " ),

    html.Div(
        children=[
            html.P(
                children='''Hello and welcome to this dash-board. 
             This website is for visulising data on Natural Gas colected form Free sources on the Web. 
             This consists of two sections: '''
             ),
            html.Ul(children=[
                html.Li(children="Natural Gas Storage"),
                html.Li(children="Natural Gas Production"),
            ]),
            html.P(
                children='''Currently Natural Gas stoage and prices are in the news due to number 
                of factors which I will try to visulise in this website. '''
             ),
            ], className="home-context",
        ),
    html.Div(children=[
           html.H2(children='Natural Gas Storage'),
            ],
            className="card"
            ),
    html.Div(children=[
                html.H2(children='Natural Gas Production', className="home-sub-sub-heading"),
                html.Div(
                    children=[
                        html.Div(
                            children = dcc.Graph(
                                id="consumtion-chart", 
                                config={"displayModeBar":False},
                                figure={
                                    "data": [
                                        {
                                            "x": cont_data["Date"],
                                            "y": cont_data["Dry natural gas production,{}, Annual".format(continent)],
                                            "type": "bar",
                                            "name": continent,                          
                                            "hovertemplate": (
                                                "%{y:.2f}<extra></extra>"
                                            ),
                                        }
                                        for continent in continents
                                    ],
                                    "layout": {
                                        "title": {
                                            "text": "Yearly Production by Continent",
                                            "x": 0.05,
                                            "xanchor": "left",
                                        },
                                        "xaxis": {"fixedrange": True},
                                        "yaxis": {
                                            "title": "Yearly Production[BCF]",
                                            "fixedrange": True,
                                        },
                                        #"colorway": ["#17b897"],
                                        "barmode": "stack"
                                    },
                                },
                            ),
                            className = "home-card",
                            id = "prod",
                        ),
                        html.Div(children=["BHA"],id="prodText"),
                        html.Div(children=["BHA"],id="resText"),
                        html.Div(
                            html.Div(
                            children = dcc.Graph(
                                id="cont-storage-chart", 
                                config={"displayModeBar":False},
                                figure={
                                    "data": [
                                        {
                                            "x": cont_data["Date"],
                                            "y": cont_data["Natural gas reserves,{}, Annual".format(continent)],
                                            "type": "bar",
                                            "name": continent,                          
                                            "hovertemplate": (
                                                "%{y:.2f}<extra></extra>"
                                            ),
                                        }
                                        for continent in continents
                                    ],
                                    "layout": {
                                        "title": {
                                            "text": "Natural Gas Reserves by Continent",
                                            "x": 0.05,
                                            "xanchor": "left",
                                        },
                                        "xaxis": {"fixedrange": True},
                                        "yaxis": {
                                            "title": "Yearly Production[TCF]",
                                            "fixedrange": True,
                                        },
                                        #"colorway": ["#17b897"],
                                        "barmode": "stack"
                                    },
                                },
                            ),
                            className = "home-card",
                            id="res",
                            ),
                        ),
                        
                    ],
                ),
            ],
            className="home-wrapper"
            ),
    ]
)