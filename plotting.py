#This script plots all cab trips from a given zone in a given month, with total fare as a function of time of day

import pandas
import numpy
import matplotlib
import datetime

green = pandas.read_csv("Data - Green Cabs/green_tripdata_2019-09.csv", header=0, usecols=["lpep_pickup_datetime", "PULocationID", "total_amount"])
green = green.rename(columns={'lpep_pickup_datetime': 'datetime', 'PULocationID': 'pickupzone', 'total_amount': 'totalfare'})
yellow = pandas.read_csv("Data - Yellow Cabs/yellow_tripdata_2019-09.csv", header=0, usecols=["tpep_pickup_datetime", "PULocationID", "total_amount"])
yellow = yellow.rename(columns={'tpep_pickup_datetime': 'datetime', 'PULocationID': 'pickupzone', 'total_amount': 'totalfare'})
d=pandas.concat([green, yellow])
d["datetime"] = pandas.to_datetime(d['datetime'], format='%Y-%m-%d %H:%M:%S')
d["datetime"] = d["datetime"].apply(lambda x: x.replace(2000, 1, 1))
d = d[d['totalfare'] < 300]
d = d[d['totalfare'] > 0]
d = d[d['pickupzone'] == 20]
d.plot.scatter(x="datetime", y="totalfare")
matplotlib.pyplot.show()