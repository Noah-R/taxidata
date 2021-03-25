#todo: sort all of this into functions
import pandas as pd
import datetime
used_cols=["lpep_pickup_datetime", "PULocationID", "passenger_count", "fare_amount", "extra", "mta_tax", "tip_amount", "tolls_amount", "improvement_surcharge", "total_amount", "payment_type", "congestion_surcharge"]
validation_cols=["trip_distance"]
d = pd.read_csv("Data/Data - Green Cabs/green_tripdata_2019-01_truncated.csv", header=0, usecols=used_cols+validation_cols)
d["lpep_pickup_datetime"] = pd.to_datetime(d['lpep_pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
d = d[d["lpep_pickup_datetime"]>datetime.datetime(year=2019, day=1, month=1)]
d = d[d["lpep_pickup_datetime"]<datetime.datetime(year=2020, day=1, month=1)]
d = d[d["fare_amount"]>0]
d = d[d["fare_amount"]<300]
d = d[d[["PULocationID"]]>0]
d = d[d[["PULocationID"]]<264]
d = d[d[["trip_distance"]]>0]
d = d[d[["trip_distance"]]<100]
print(d.head())