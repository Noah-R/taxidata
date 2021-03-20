#This script takes the results from counting.py for a number of zones, and graphs them over the course of the day, normalized as a percentage of all trips in the zone for comparison purposes
#It might make more sense to move the tabulating of percentages to the counting file, but for current purposes it works either way
import pandas
import numpy
import matplotlib
import datetime

chosenzones=["20", "31", "47"]
d=pandas.read_csv("Tables/"+chosenzones[0]+" results.csv", usecols=["TimeBucket", "Amount"])
d[chosenzones[0]] = d["Amount"].apply(lambda x: x/d["Amount"].sum())
#d=d.rename(columns={'Amount': chosenzones[0]})#this replaces the above line if not normalizing for comparison purposes
for i in range(1, len(chosenzones)):
    d2=pandas.read_csv("Tables/"+chosenzones[i]+" results.csv", usecols=["TimeBucket", "Amount"])
    d2[chosenzones[i]] = d2["Amount"].apply(lambda x: x/d2["Amount"].sum())
    #d2=d2.rename(columns={'Amount': chosenzones[i]})#this replaces the above line if not normalizing for comparison purposes
    d = pandas.merge(d, d2, on="TimeBucket")
d["TimeBucket"] = pandas.to_datetime(d['TimeBucket'], format='%Y-%m-%d %H:%M:%S')
d.plot(x="TimeBucket", y=chosenzones)
matplotlib.pyplot.show()