import pandas
import numpy
import matplotlib
import datetime

chosenzone=20
d=pandas.read_csv("Graphs/"+str(chosenzone)+" results.csv")
d["TimeBucket"] = pandas.to_datetime(d['TimeBucket'], format='%Y-%m-%d %H:%M:%S')
d.plot.scatter(x="TimeBucket", y="Amount")
matplotlib.pyplot.show()