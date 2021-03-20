#This script iterates through every trip all year, and for a given set of zones, counts up the number of hails, and the percentage of all hails, during each quarter hour of the day. Results are exported to CSV's, which are graphed in plotting.py.
#Further expansions of this could include narrowing results by day of week, weather, other trip metadata
import pandas
import numpy
import datetime

chosenzones=["31", "20", "47", "18"]
frames={}
for i in range(len(chosenzones)):
    data = {'TimeBucket': [], 'Amount': []}
    for time in range(96):
        data["TimeBucket"].append(datetime.datetime(year=2000, month=1, day=1, hour=int(time/4), minute=time%4*15))
        data["Amount"].append(0)
    frame = pandas.DataFrame.from_dict(data)
    frames[chosenzones[i]]=frame

filenames=[]
for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
    print("Starting month "+month)
    green = pandas.read_csv("Data - Green Cabs/green_tripdata_2019-"+month+".csv", header=0, usecols=["lpep_pickup_datetime", "PULocationID"])
    green = green.rename(columns={'lpep_pickup_datetime': 'datetime', 'PULocationID': 'pickupzone'})
    yellow = pandas.read_csv("Data - Yellow Cabs/yellow_tripdata_2019-"+month+".csv", header=0, usecols=["tpep_pickup_datetime", "PULocationID"])
    yellow = yellow.rename(columns={'tpep_pickup_datetime': 'datetime', 'PULocationID': 'pickupzone'})
    d=pandas.concat([green, yellow])
    green = None
    yellow = None
    d = d[d['pickupzone'].apply(lambda x: str(x)).isin(chosenzones)]
    d["datetime"] = pandas.to_datetime(d['datetime'], format='%Y-%m-%d %H:%M:%S')
    d["datetime"] = d["datetime"].apply(lambda x: x.replace(2000, 1, 1))
    for index, row in d.iterrows():
        zone=str(row["pickupzone"])
        time=row["datetime"].replace(2000, 1, 1)
        frame=frames[zone]
        for i2, r2 in frame.iterrows():
            if(time<=r2["TimeBucket"]+datetime.timedelta(minutes=15)):
                frame.loc[i2,"Amount"]+=1
                break

for zone in chosenzones:
    frame=frames[zone]
    total = frame["Amount"].sum()
    frame["Percentage"] = frame["Amount"].apply(lambda x: x/total)
    frame.to_csv("Tables/"+zone+" results.csv")