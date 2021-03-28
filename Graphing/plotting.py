#This script takes the results from counting.py for a number of zones, and graphs them over the course of the day. It can be configured to show trips as either raw totals, or as a percentage of total trips for comparison purposes.
import pandas
import numpy
import matplotlib
import datetime

totaltype="Percentage"#"Percentage" or "Amount"
chosenzones=["20", "31", "47", "18"]
d=pandas.read_csv("Tables/"+chosenzones[0]+" results.csv", usecols=["TimeBucket", totaltype])
d=d.rename(columns={totaltype: chosenzones[0]})
for i in range(1, len(chosenzones)):
    d2=pandas.read_csv("Tables/"+chosenzones[i]+" results.csv", usecols=["TimeBucket", totaltype])
    d2=d2.rename(columns={totaltype: chosenzones[i]})
    d = pandas.merge(d, d2, on="TimeBucket")
d["TimeBucket"] = pandas.to_datetime(d['TimeBucket'], format='%Y-%m-%d %H:%M:%S')
d["TimeBucket"] = d["TimeBucket"].apply(lambda x: x.time())
d.plot(x="TimeBucket", y=chosenzones)
matplotlib.pyplot.show()