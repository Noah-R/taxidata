#This script iterates through every trip all year, and for a given set of zones, counts up the number of hails, and the percentage of all hails, that resulted in meter fares(time and distance, not counting taxes, surcharges, tolls, or tips) of each dollar amount, rounded down. Results are exported to CSV's, which are graphed in plotting.py.
import pandas
import numpy
import datetime

chosenzones=["31"]

data = {'FareBucket': [], 'Amount': []}
for dollars in range(301):
    data["FareBucket"].append(dollars)
    data["Amount"].append(0)
frame = pandas.DataFrame.from_dict(data)

filenames=[]
for month in ["01"]:#, "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:#unmodify
    print("Reading in month "+month)
    green = pandas.read_csv("Data/Data - Green Cabs/green_tripdata_2019-"+month+".csv", header=0, usecols=["fare_amount", "PULocationID"])
    green = green.rename(columns={'fare_amount': 'total', 'PULocationID': 'pickupzone'})
    yellow = pandas.read_csv("Data/Data - Yellow Cabs/yellow_tripdata_2019-"+month+".csv", header=0, usecols=["fare_amount", "PULocationID"])
    yellow = yellow.rename(columns={'fare_amount': 'total', 'PULocationID': 'pickupzone'})
    d=pandas.concat([green, yellow])
    green = None
    yellow = None

    #d = d[d['pickupzone'].apply(lambda x: str(x)).isin(chosenzones)]#undelete
    d = d[d['total'].apply(lambda x: x<300 and x>0)]

    for index, row in d.iterrows():
        frame.loc[int(row["total"]),"Amount"]+=1

total = frame["Amount"].sum()
frame["Percentage"] = frame["Amount"].apply(lambda x: x/total)
zones=""
for zone in chosenzones:
    zones+=zone+", "
zones=zones[:-2]
zones="january"#delete
frame.to_csv("Tables-/"+str(zones)+" results.csv")