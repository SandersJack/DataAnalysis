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
           html.Div(children=[
                html.P('''Demand for Natural Gas can vary across the year, mainly dependent on temperature. In Europe, this is more apparent due to the cold winters and mild summers (But this could change as global temperature trends upwards!).
                       When the weather is cold, natural gas consumption increases due to the electricity demand associated with heating homes/businesses. In the hotter months, 
                       Natural Gas consumption will increase due to the electricity demand associated with cooling homes and businesses with Air Conditioning. However, usually, the demand in the winter is much greater. 
                       If countries/companies didn't store any Natural Gas and only used it from the free market, the price would also fluctuate drastically due to the increased demand and steady supply'''),
                html.P('''Natural Gas Storage can be classified into underground and surface storage. Underground is the most extensively used because of the larger storage sizes, utilising old mines or old Gas/Oil deposits to store Gas. 
                       Surface storage is used less and is usually more expensive, requiring large pressurised storage tanks to be used. These are more likely to be used by companies rather than countries.'''),
                html.P(children='''In the Natural Gas Storage section, you will find Natural Gas storage data for European countries between March 2011 to March 2023. Data includes Natural Gas storage levels, Injection and withdrawals and bi-annual consumption.'''),
            ], className="storage-text"
            ), 
            ],
            className="home-wrapper", 
            id="storage"
            ),
    html.Div(children=[
                html.H2(children='Natural Gas Production', className="home-sub-sub-heading"),
                html.Div(children=[
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
                        html.Div(children=[
                            html.P(children='''Natural Gas is produced across the world in all seven inhabited continents. 
                                   Two states dominate the world's production; The United States of America (USA) and Russia. The largest production can be found in North America. There are several ways Natural Gas can be produced/extracted:'''),
                            html.P(children='''There are a number of ways Natural Gas can be produced/extracted:'''),
                            html.H3(children="Conventional Extraction:"),
                            html.P(children='''Natural Gas can be found together with oil under a permeable layer of rock. 
                                   This is beneficial as this allows both the extraction of Natural Gas and oil, reducing the cost.'''),
                            html.H3(children="Un-Conventional Extraction:"),
                            html.P(children='''This gas is found deep underground, making it expensive and practically tricky. Only because of recent advancements has this option become more viable. 
                                   One type of extraction you might be aware of is fracking, which is the process of extracting Tight Gas. 
                                   Now this is controversial in the UK due to its links to earthquakes.'''),
                            html.P(children='''These unconventional methods of production will become more previlent as the cheaper and easier to extract Natural Gas reserves run out.'''),
                            html.P(children='''In the production tab you will find yearly extraction (withdrawls) and export data. As well as a monthly reports for the USA and Canada'''),

                            ],id="prodText"),
                        ], className="top-prod"),
                        html.Div(children=[
                            html.H3(children="Proven Reserves:"),
                            html.P(children='''The largest proven Natural Gas reserves can be found in the Middle East and Eurasia. Mainly located in Russia, Iran and Qatar, making up just over half of the worlds proven supplies. 
                                   As mentioned above there is the possibly of these reserves to increase as technology imporves to extract harder to get Natural Gas. But it is still a finite resource that will one day run out'''),
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
                            ],id="resText"),
                        html.Div( children = [
                            html.Div(
                            children = dcc.Graph(
                                id="full-export-chart", 
                                config={"displayModeBar":False},
                                figure={
                                    "data": [
                                        {
                                            "x": cont_data["Date"].loc[(cont_data["Date"] >= "1990")],
                                            "y": cont_data["Dry natural gas exports,{}, Annual".format(continent)].loc[(cont_data["Date"] >= "1990")],
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
                                            "text": "Natural Gas Export by Continent",
                                            "x": 0.05,
                                            "xanchor": "left",
                                        },
                                        "xaxis": {"fixedrange": True},
                                        "yaxis": {
                                            "title": "Yearly Export[TCF]",
                                            "fixedrange": True,
                                        },
                                        #"colorway": ["#17b897"],
                                        "barmode": "stack"
                                    },
                                },
                            ),
                            
                            className = "home-card",
                            ),
                        html.H3(children="Exports:"),
                        html.P(children='''Even though The United States produces the most Natural Gas, it barely exports it. 
                                   This is due to a couple of factors: 1) It is one of the biggest consumers of Natural Gas, so its domestic demand still outpaces its production. And 2) they are far away from other large consumers of Natural Gas. Meaning that it needs to be exported as Liquified Natural Gas (LNG) by ship, which is expensive.
                                   Making their Gas more costly for European customers, for example, who previously could buy Russian Gas at a lower price due to the extensive European pipeline network.'''),
                        ],
                                 id="export-chart",
                        ),
                        
                    ],
                ),
            ],
            className="home-wrapper"
            ),
    ]
)