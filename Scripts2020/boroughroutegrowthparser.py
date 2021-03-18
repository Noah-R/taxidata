#This script reads data from June 2018 and June 2019, and analyzes the year over year change in boroughs travelled. The final report is sorted from largest decline to largest growth.
import csv
import boroughparser
l=[]
boroughs=boroughparser.getBoroughs()
boroughcombinations=boroughparser.getCombinations()
for i in range(7):
    l.append([])
    for j in range(7):
        l[i].append([0, 0])
zones=boroughparser.getZones()
for zone in zones:
    for i in range(7):
        if(zone[1]==boroughs[i]):
            zone.append(i)
            break
resultsfile=open("boroughroutegrowthresults.txt", "w")
totals=[]
startyear=18#change to 16 for fuller results, will need to reconcile inconsistent data headers
for i in range(startyear, 20):
    count=0
    y=open("yellow06"+str(i)+".csv")
    g=open("green06"+str(i)+".csv")
    readery=csv.reader(y)
    for row in readery:
        try:
         #1 for trips
            #row[4] for miles
            #row[16] for dollars
            l[zones[int(row[7])-1][2]][zones[int(row[8])-1][2]][i-startyear]+=1
            count+=1
        except:
            print(row)
    print("parsed yellow "+str(i))
    readerg=csv.reader(g)
    for row in readerg:
        try:
            #1 for trips
            #row[8] for miles
            #row[16] for dollars
            l[zones[int(row[5])-1][2]] [zones[int(row[6])-1][2]][i-startyear]+=1
            count+=1
        except:
            print(row)
    print("parsed green "+str(i))
    y.close()
    g.close()
    totals.append(count)
for a in range(6):
    for b in range(6):
        resultsfile.write("Trips from "+boroughs[a]+" to "+boroughs[b]+" progressed "+str(l[a][b])+"\n")
resultsfile.write("Total trips progressed "+str(totals))
resultsfile.close()