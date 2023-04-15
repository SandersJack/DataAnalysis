import requests 
import csv
from datetime import date, timedelta
import Constants
import os


csv_t = True

if csv_t:
    os.remove("dataSets/NatStorage_Full.csv") 
    w = csv.writer(open("dataSets/NatStorage_Full.csv", 'w'))
    w.writerow(["Country","Date","Consumption [Twh]","Gas in storage [TWh]","full [%]","Injection [GWh/d]","Injection capacity [GWh/d]","Withdrawal [GWh/d]","Withdrawal capacity [GWh/d]"])

headers = {"x-key": Constants.AGSI_API_KEY}
url = 'https://agsi.gie.eu/api'

full = []
date_ = []
name = []
gas = []
inj = []
inj_cap = []
withdraw = []
withdraw_cap = [] 
consumption = []
    
start_date = date(2011, 4, 12)
end_date = date(2023, 4, 13)
delta = timedelta(days=1)
while start_date <= end_date:
    date_s = start_date.strftime("%Y-%m-%d")
    print(date_s)
    start_date += delta

    parameters = {
        "date": date_s
    }

    req = requests.get(url, headers=headers, params=parameters)


    import json

    def jprint(obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)
        
        
    print(req.json()['data'][0]['gasDayStart'])

    ##### For EU
    name.append(req.json()['data'][0]['name'])
    full.append(req.json()['data'][0]['full'])
    date_.append(req.json()['data'][0]['gasDayStart'])
    gas.append(req.json()['data'][0]["gasInStorage"])
    inj.append(req.json()['data'][0]["injection"])
    withdraw.append(req.json()['data'][0]["withdrawal"])
    inj_cap.append(req.json()['data'][0]["injectionCapacity"])
    withdraw_cap.append(req.json()['data'][0]["withdrawalCapacity"])
    consumption.append(req.json()['data'][0]["consumption"])
    w.writerow([name[-1],date_[-1],consumption[-1],gas[-1],full[-1],inj[-1],inj_cap[-1],withdraw[-1],withdraw_cap[-1]])

    for i in range(len(req.json()['data'][0]['children'])):
        name.append(req.json()['data'][0]['children'][i]['name'])
        full.append(req.json()['data'][0]['children'][i]['full'])
        date_.append(req.json()['data'][0]['children'][i]['gasDayStart'])
        gas.append(req.json()['data'][0]['children'][i]["gasInStorage"])
        inj.append(req.json()['data'][0]['children'][i]["injection"])
        withdraw.append(req.json()['data'][0]['children'][i]["withdrawal"])
        inj_cap.append(req.json()['data'][0]['children'][i]["injectionCapacity"])
        withdraw_cap.append(req.json()['data'][0]['children'][i]["withdrawalCapacity"])
        consumption.append(req.json()['data'][0]['children'][i]["consumption"])
        if csv_t:
            w.writerow([name[-1],date_[-1],consumption[-1],gas[-1],full[-1],inj[-1],inj_cap[-1],withdraw[-1],withdraw_cap[-1]])
    