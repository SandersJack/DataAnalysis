import requests 
from datetime import date, timedelta
import csv
import Constants
import json
import os
import pandas as pd

csv_t = True

if csv_t:
    os.remove("dataSets/CityTemp.csv") 
    w = csv.writer(open("dataSets/CityTemp.csv", 'w'))
    w.writerow(["Country","City","Date","tmp_min","tmp_max"])
    
cities = pd.read_csv("dataSets/eu_cities.csv")

for index, row in cities.iterrows():
    

    date_ = []
    Country_ = []
    City_ = []
    tmp_ = []

    start_date = date(2011, 4, 12)
    end_date = date(2023, 1, 30)

    lat = row['lat']
    long = row['lng']

    country = row['country']
    city = row['city']

    print(country)

    url = 'https://archive-api.open-meteo.com/v1/archive?latitude={}&longitude={}&start_date={}&end_date={}&hourly=temperature_2m'.format(lat,long,start_date,end_date)

    req = requests.get(url)

    prevyear = 0
    for i in range(len(req.json()["hourly"]['time'])):
        time = req.json()["hourly"]['time'][i][11:]
        dateT = req.json()["hourly"]['time'][i][:10]
        year = req.json()["hourly"]['time'][i][:4]
        if year != prevyear:
            print(year)
        tmp_.append(req.json()["hourly"]['temperature_2m'][i])
        Country_.append(country)
        City_.append(city)
        prevyear = year
        if time == "23:00":
            tmp_min = min(tmp_)
            tmp_max = max(tmp_)  
            tmp_ = []
            if csv_t:
                w.writerow([Country_[-1],City_[-1],dateT,tmp_min,tmp_max])