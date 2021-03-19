import pandas
import numpy
import matplotlib
import datetime

chosenzones=["20", "31"]
d=pandas.read_csv("Tables/"+chosenzones[0]+" results.csv", usecols=["TimeBucket", "Amount"])
d=d.rename(columns={'Amount': chosenzones[0]})
for i in range(1, len(chosenzones)):
    d2=pandas.read_csv("Tables/"+chosenzones[i]+" results.csv", usecols=["TimeBucket", "Amount"])
    d2=d2.rename(columns={'Amount': chosenzones[i]})
    d = pandas.merge(d, d2, on="TimeBucket")
d["TimeBucket"] = pandas.to_datetime(d['TimeBucket'], format='%Y-%m-%d %H:%M:%S')
d.plot(x="TimeBucket", y=chosenzones)
matplotlib.pyplot.show()