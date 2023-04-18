import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(children='Welcome to this Dash-Board'),

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
            ],
        ),
    html.Div(children=[
           html.H2(children='Natural Gas Storage') 
            ],
            className="card"
        ),
    html.Div(children=[
           html.H2(children='Natural Gas Production') 
            ],
            className="card"
        ),
    ]
)