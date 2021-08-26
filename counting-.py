#This script iterates through every trip all year, and for a given set of zones, counts up the number of hails, and the percentage of all hails, that resulted in pre-tip fares of each dollar amount, rounded down. Results are exported to CSV's, which are graphed in plotting.py.
import pandas
import numpy
import datetime

chosenzones=["31"]

data = {'FareBucket': [], 'Amount': []}
for dollars in range(201):
    data["FareBucket"].append(dollars)
    data["Amount"].append(0)
frame = pandas.DataFrame.from_dict(data)

filenames=[]
for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
    print("Starting month "+month)
    green = pandas.read_csv("Data/Data - Green Cabs/green_tripdata_2019-"+month+".csv", header=0, usecols=["total_amount", "tip_amount", "PULocationID"])
    green = green.rename(columns={'total_amount': 'total', 'tip_amount': 'tip', 'PULocationID': 'pickupzone'})
    yellow = pandas.read_csv("Data/Data - Yellow Cabs/yellow_tripdata_2019-"+month+".csv", header=0, usecols=["total_amount", "tip_amount", "PULocationID"])
    yellow = yellow.rename(columns={'total_amount': 'total', 'tip_amount': 'tip', 'PULocationID': 'pickupzone'})
    d=pandas.concat([green, yellow])
    green = None
    yellow = None
    d = d[d['pickupzone'].apply(lambda x: str(x)).isin(chosenzones)]

    for index, row in d.iterrows():
        fare=row["total"]-row["tip"]
        for i2, r2 in frame.iterrows():
            if(fare<r2["FareBucket"]+1 or r2["FareBucket"]==200):
                frame.loc[i2,"Amount"]+=1
                break

total = frame["Amount"].sum()
frame["Percentage"] = frame["Amount"].apply(lambda x: x/total)
zones=""
for zone in chosenzones:
    zones+=zone+", "
zones=zones[:-2]
frame.to_csv("Tables-/"+str(zones)+" results.csv")