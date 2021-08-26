#This script takes the results from counting.py for a number of zones, and graphs the distribution of fare amounts. It can be configured to show trips as either raw totals, or as a percentage of total trips for comparison purposes.
import pandas
import numpy
import matplotlib
import datetime

totaltype="Amount"#"Percentage" or "Amount"
chosenzones=["31"]
zones=""
for zone in chosenzones:
    zones+=zone+", "
zones=zones[:-2]
d=pandas.read_csv("Tables-/"+zones+" results.csv", usecols=["FareBucket", totaltype])
d.plot(x="FareBucket", y=totaltype)
matplotlib.pyplot.show()