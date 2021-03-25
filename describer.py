#A rough and dirty script that uses pd.describe() to compare overviews between two different month-category combinations. Edit column and file names to your liking.
import pandas as pd
cols=["trip_distance", "passenger_count", "payment_type", "fare_amount", "extra", "mta_tax", "tip_amount", "tolls_amount", "improvement_surcharge", "total_amount", "congestion_surcharge"]
d = pd.read_csv("Data/Data - Yellow Cabs/yellow_tripdata_2019-01.csv", header=0, usecols=cols) 
d2 = pd.read_csv("Data/Data - Yellow Cabs/yellow_tripdata_2019-07.csv", header=0, usecols=cols) 

d=d[d["trip_distance"]>0]
d=d[d["fare_amount"]>0]
d2=d2[d2["trip_distance"]>0]
d2=d2[d2["fare_amount"]>0]
for col in cols:
    print(col)
    print("First")
    print(d[col].describe())
    print("Second")
    input(d2[col].describe())