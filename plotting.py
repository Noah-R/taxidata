#This script plots all green cab trips on a given date, with total fare as a function of time of day

import pandas
import numpy
import matplotlib
import datetime

name = "Data - Green Cabs/green_tripdata_2019-01.csv"
d = pandas.read_csv(name, header=0, usecols=["lpep_pickup_datetime", "total_amount"])
d["lpep_pickup_datetime"] = pandas.to_datetime(d['lpep_pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
d = d[d['lpep_pickup_datetime'] > datetime.datetime(year=2019, month=1, day=20)]
d = d[d['lpep_pickup_datetime'] < datetime.datetime(year=2019, month=1, day=21)]
d = d[d['total_amount'] < 300]
d = d[d['total_amount'] > 0]
d.plot.scatter(x="lpep_pickup_datetime", y="total_amount")
matplotlib.pyplot.show()