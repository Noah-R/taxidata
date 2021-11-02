import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn.cluster import Kmeans

def getfilenames():
    filenames=[]
    for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
        filenames.append("Data/Data - Yellow Cabs/yellow_tripdata_2019-"+month+".csv")
        filenames.append("Data/Data - Green Cabs/green_tripdata_2019-"+month+".csv")
    return filenames

def preprocess(filename, nrows=-1):
    #if nrows is passed, exclude all but a randomly selected nrows number of rows
    linesinfile=sum(1 for line in open(filename))
    if(nrows>0 and nrows<linesinfile-1):
        exclude = []
        for n in range(1, linesinfile):
            exclude.append(n)
        for n in range(nrows):
            exclude.pop(random.randint(0, len(exclude)-1))
    elif(nrows==0):
        return None
    else:
        exclude=None

    #decide which columns to use
    preprocessing_cols=["total_amount", "tip_amount"]
    used_cols=["trip_distance", "passenger_count"]

    #read in the trip data
    d = pd.read_csv(filename, header=0, usecols=used_cols+preprocessing_cols, skiprows=exclude)

    #exclude tips from fare, since cash tips are unknown
    d["fare"] = d.apply(lambda row: float(row["total_amount"]) - float(row["tip_amount"]), axis=1)

    #remove rows with obvious data errors
    d = d[d["fare_amount"]>0]
    d = d[d["fare_amount"]<300]
    d = d[d["trip_distance"]>0]
    d = d[d["trip_distance"]<100]
    d = d.drop(preprocessing_cols, axis=1)

    #drop columns not used to predict
    d = d.drop(preprocessing_cols, axis=1)

    return d

def makesample(yellowcount=50000, greencount=5000):
    filenames=getfilenames()
    data=None
    for name in filenames:
        if("green" in name):
            rows=greencount
        elif("yellow" in name):
            rows=yellowcount
        else:
            rows=0
            print("something went wrong")
        print("Starting "+name)#todo remove
        data = pd.concat([data, preprocess(filename=name, nrows=rows)])
    data = data.dropna(axis=0)
    return data

makesample(1000, 100).to_csv("sample.csv")

data = pd.read_csv("sample.csv", header=0)

model = KMeans(
                    n_clusters=3,
                    init='k-means++', 
                    max_iter=500, 
                    random_state=0)
model.fit_predict(data)