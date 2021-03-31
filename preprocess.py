import pandas as pd
import datetime
import random

def preprocess(filename, nrows=0):
    #if nrows is passed, exclude all but a randomly selected nrows number of rows
    if(nrows>0):
        exclude = []
        for n in range(1, sum(1 for line in open(filename))):
            exclude.append(n)
        for n in range(nrows):
            exclude.pop(random.randint(1, len(exclude)))
    else:
        exclude=None

    #handle header inconsistency between green/yellow
    if("yellow_tripdata" in filename):
        pickupcolumn="tpep_pickup_datetime"
    elif("green_tripdata" in filename):
        pickupcolumn="lpep_pickup_datetime"
    else:
        return("something is seriously wrong")

    #decide which columns to use
    used_cols=[pickupcolumn, "PULocationID", "passenger_count"]
    preprocessing_cols=["tip_amount", "total_amount","fare_amount", "trip_distance"]

    #read in the trip data
    d = pd.read_csv(filename, header=0, usecols=used_cols+preprocessing_cols, skiprows=exclude)
    d = d.rename({pickupcolumn: "datetime"}, axis=1)
    d["datetime"] = pd.to_datetime(d['datetime'], format='%Y-%m-%d %H:%M:%S')
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
    d = d.drop(preprocessing_cols, axis=1)

    #split datetime column into three more usable pieces
    d["date"] = d["datetime"].apply(lambda x: x.date())
    d["time"] = d["datetime"].apply(lambda x: x.time())
    d["weekday"] = d["datetime"].apply(lambda x: x.weekday()<5)
    d = d.drop("datetime", axis=1)

    #join weather data along date
    joiner = pd.read_csv("Data/Data - Background Tables/Weather.csv", header=0, usecols=["MONTH", "DAY", "FED HOLIDAY", "High Temperature", "Low Temperature", "Average Temperature", "Precipitation", "Snow"])
    joiner["date"] = joiner.apply(lambda row: datetime.date(year=2019, month=int(row["MONTH"]), day=int(row["DAY"])), axis=1)
    joiner = joiner.drop(["MONTH", "DAY"], axis=1)
    joiner = joiner.set_index("date")
    d = d.join(joiner, on="date")

    #join nta's along tlc zones
    joiner = pd.read_csv("Data/Data - Background Tables/Zones to NTA's.csv", header=0, usecols=["TLC Zone", "NTA Code"], index_col="TLC Zone")
    d = d.join(joiner, on="PULocationID")

    #join nta data along nta's
    joiner = pd.read_csv("Data/Data - Background Tables/Demographics, Population, Income.csv", header=0, index_col="NTA Code", usecols=["NTA Code", "Per Acre", "Median Household Income", "Mean Household Income", "Median Age", "Hispanic%", "White%", "Black%", "Asian%", "Other%", "Multiracial%"])
    d = d.join(joiner, on="NTA Code")

    #Count federal holidays as weekends
    d["weekday"] = d.apply(lambda row: row["weekday"] and row["FED HOLIDAY"] == 0, axis=1)

    #drop columns not used to predict
    d = d.drop(["PULocationID", "NTA Code", "FED HOLIDAY"], axis=1)

    return d

data=preprocess("Data/Data - Yellow Cabs/yellow_tripdata_2019-12.csv", nrows=10)
data.to_csv("results.csv")