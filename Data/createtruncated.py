#This script makes versions of the csv's with only 10 lines each. This is so I can actually open them and look at the format without running out of memory.
import pandas
filenames=[]
for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
    filenames.append("Data - Green Cabs/green_tripdata_2019-"+month+".csv")
    filenames.append("Data - Yellow Cabs/yellow_tripdata_2019-"+month+".csv")
for f in filenames:
    r=pandas.read_csv(f, nrows=10, header=0)
    r.to_csv(f[:-4]+"_truncated.csv")