import pandas as pd
import datetime

#decide which columns to use and read in the data
used_cols=["lpep_pickup_datetime", "PULocationID", "passenger_count", "tip_amount", "total_amount"]
validation_cols=["trip_distance", "fare_amount"]
d = pd.read_csv("Data/Data - Green Cabs/green_tripdata_2019-01.csv", header=0, usecols=used_cols+validation_cols)
d["lpep_pickup_datetime"] = pd.to_datetime(d['lpep_pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
d["date"] = d["lpep_pickup_datetime"].apply(lambda x: x.date())

#remove rows with obvious data errors
d = d[d["lpep_pickup_datetime"]>=datetime.datetime(year=2019, day=1, month=1)]
d = d[d["lpep_pickup_datetime"]<datetime.datetime(year=2020, day=1, month=1)]
d = d[d["fare_amount"]>0]
d = d[d["fare_amount"]<300]
d = d[d["PULocationID"]>0]
d = d[d["PULocationID"]<264]
d = d[d["trip_distance"]>0]
d = d[d["trip_distance"]<100]
d = d.drop(validation_cols, axis=1)

#join nta's along tlc zones
joiner = pd.read_csv("Data/Data - Background Tables/Zones to NTA's.csv", header=0, usecols=["TLC Zone", "NTA Code"], index_col="TLC Zone")
d = d.join(joiner, on="PULocationID")

#join nta data along nta's
joiner = pd.read_csv("Data/Data - Background Tables/Demographics, Population, Income.csv", header=0, index_col="NTA Code")
joiner = joiner.drop(["Neighborhood Name", "Borough"], axis=1)
d = d.join(joiner, on="NTA Code")

#join weather data along date
joiner = pd.read_csv("Data/Data - Background Tables/Weather.csv", header=0)
joiner = joiner.drop(["FED HOLIDAY", "AVG SPD", "MX SPD", "2MIN DIR", "WX"], axis=1)
joiner["date"] = joiner.apply(lambda row: datetime.date(year=2019, month=row["MONTH"], day=row["DAY"]), axis=1)
joiner = joiner.set_index("date")
d = d.join(joiner, on="date")

#show results
d.to_csv("results.csv")