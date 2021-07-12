import pandas as pd
import datetime
import random
import statsmodels.api as sm
import matplotlib.pyplot as plt

def getfilenames():
    filenames=[]
    for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
        filenames.append("Data/Data - Yellow Cabs/yellow_tripdata_2019-"+month+".csv")
        filenames.append("Data/Data - Green Cabs/green_tripdata_2019-"+month+".csv")
    return filenames

def preprocess(filename, nrows=-1):
    #if nrows is passed, exclude all but a randomly selected nrows number of rows
    linesinfile=sum(1 for line in open(filename))
    if(nrows>0 and nrows<linesinfile-1):
        exclude = []
        for n in range(1, linesinfile):
            exclude.append(n)
        for n in range(nrows):
            exclude.pop(random.randint(0, len(exclude)-1))
    elif(nrows==0):
        return None
    else:
        exclude=None

    #handle header inconsistency between green/yellow
    if("yellow_tripdata" in filename):
        pickupcolumn="tpep_pickup_datetime"
        dropoffcolumn="tpep_dropoff_datetime"
    elif("green_tripdata" in filename):
        pickupcolumn="lpep_pickup_datetime"
        dropoffcolumn="lpep_dropoff_datetime"
    else:
        return("something is seriously wrong")
        #these lines will obviously never run but they fix some undefined warnings
        pickupcolumn="lpep_pickup_datetime"
        dropoffcolumn="lpep_dropoff_datetime"

    #decide which columns to use
    used_cols=[pickupcolumn, dropoffcolumn, "PULocationID", "passenger_count"]
    preprocessing_cols=["tip_amount", "total_amount","fare_amount", "trip_distance"]

    #read in the trip data
    d = pd.read_csv(filename, header=0, usecols=used_cols+preprocessing_cols, skiprows=exclude)
    d = d.rename({pickupcolumn: "datetime", dropoffcolumn: "endtime"}, axis=1)
    d["datetime"] = pd.to_datetime(d['datetime'], format='%Y-%m-%d %H:%M:%S')
    d["endtime"] = pd.to_datetime(d['endtime'], format='%Y-%m-%d %H:%M:%S')
    d["length"] = d.apply(lambda row: (row["endtime"]-row["datetime"]).total_seconds(), axis=1)
    d["fare"] = d.apply(lambda row: float(row["total_amount"]) - float(row["tip_amount"]), axis=1)#fare includes meter plus all charges but does not include tips

    #remove rows with obvious data errors
    d = d[d["datetime"]>=datetime.datetime(year=2019, day=1, month=1)]
    d = d[d["datetime"]<datetime.datetime(year=2020, day=1, month=1)]
    d = d[d["fare_amount"]>0]
    d = d[d["fare_amount"]<300]
    d = d[d["PULocationID"]>0]
    d = d[d["PULocationID"]<264]
    d = d[d["trip_distance"]>0]
    d = d[d["trip_distance"]<100]
    d = d[d["length"]>0]
    d = d.drop(preprocessing_cols, axis=1)

    #split datetime column into three more usable pieces
    d["date"] = d["datetime"].apply(lambda x: x.date())
    d["time"] = d["datetime"].apply(lambda x: x.time())
    d["weekday"] = d["datetime"].apply(lambda x: x.weekday()<5)
    d = d.drop("datetime", axis=1)
    d = d.drop("endtime", axis=1)

    #join weather data along date
    joiner = pd.read_csv("Data/Data - Background Tables/Weather.csv", header=0, usecols=["MONTH", "DAY", "FED HOLIDAY", "High Temperature", "Low Temperature", "Average Temperature", "Precipitation", "Snow"])
    joiner["date"] = joiner.apply(lambda row: datetime.date(year=2019, month=int(row["MONTH"]), day=int(row["DAY"])), axis=1)
    joiner = joiner.drop(["MONTH", "DAY"], axis=1)
    joiner = joiner.set_index("date")
    d = d.join(joiner, on="date")

    #join nta's along tlc zones
    joiner = pd.read_csv("Data/Data - Background Tables/Zones to NTA's.csv", header=0, usecols=["TLC Zone", "NTA Code", "Borough"], index_col="TLC Zone")
    d = d.join(joiner, on="PULocationID")

    #join nta data along nta's
    joiner = pd.read_csv("Data/Data - Background Tables/Demographics, Population, Income.csv", header=0, index_col="NTA Code", usecols=["NTA Code", "Per Acre", "Median Household Income", "Mean Household Income", "Median Age", "Hispanic%", "White%", "Black%", "Asian%", "Other%", "Multiracial%"])
    d = d.join(joiner, on="NTA Code")

    #Count federal holidays as weekends and convert to int
    d["weekday"] = d.apply(lambda row: row["weekday"] and row["FED HOLIDAY"] == 0, axis=1)
    d["weekday"] = d["weekday"].astype(int)

    #One-hot encode borough
    for borough in ["Bronx", "Brooklyn", "Queens", "Manhattan", "Staten Island", "Airport"]:
        d[borough] = (d["Borough"]==borough).astype(int)

    #One-hot encode time
    six=datetime.time(hour=6)
    nine=datetime.time(hour=9)
    sixteen=datetime.time(hour=16)
    twenty=datetime.time(hour=20)
    d["Early Morning"] = (d["time"].apply(lambda x: x<six)).astype(int)
    d["Morning Rush Hour"] = (d["time"].apply(lambda x: x>=six and x<nine)).astype(int)
    d["Mid-Day"] = (d["time"].apply(lambda x: x>=nine and x<sixteen)).astype(int)
    d["Evening Rush Hour"] = (d["time"].apply(lambda x: x>=sixteen and x<twenty)).astype(int)
    d["Late Night"] = (d["time"].apply(lambda x: x>=twenty)).astype(int)

    #drop columns not used to predict
    d = d.drop(["PULocationID", "NTA Code", "FED HOLIDAY", "Borough", "date", "time"], axis=1)

    return d

def makesample(yellowcount=50000, greencount=5000):
    filenames=getfilenames()
    data=None
    for name in filenames:
        if("green" in name):
            rows=greencount
        elif("yellow" in name):
            rows=yellowcount
        else:
            rows=0
            print("something went wrong")
        print("Starting "+name)#todo remove
        data = pd.concat([data, preprocess(filename=name, nrows=rows)])
    data = data.dropna(axis=0)
    return data

makesample(200, 20).to_csv("sample.csv")

data = pd.read_csv("sample.csv", header=0)

yf = data.fare
yl = data.length
features="Mean Household Income"
"""features = ['passenger_count', 'weekday',
       'High Temperature', 'Low Temperature', 'Average Temperature',
       'Precipitation', 'Snow', 'Per Acre', 'Median Household Income',
       'Mean Household Income', 'Median Age', 'Hispanic%', 'White%', 'Black%',
       'Asian%', 'Other%', 'Multiracial%', 'Bronx', 'Brooklyn', 'Queens',
       'Manhattan', 'Staten Island', 'Airport']"""
X = data[features]

#X = sm.add_constant(X)
#faremodel = sm.OLS(yf, X).fit()
#print(faremodel.summary())

plt.scatter(X, yf)
plt.show()