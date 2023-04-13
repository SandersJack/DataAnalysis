# Author: Jack Sanders
# Created: 13/04/23

import pandas as pd
from dash import Dash, dcc, html, Input, Output

data = (
    pd.read_csv("dataSets/StorageData_GIE.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Gas Day Start"], format="%Y-%m-%d"))
    .sort_values(by="Gas Day Start")
)