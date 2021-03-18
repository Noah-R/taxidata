#This script reads data from June 2018 and June 2019, and analyzes the year over year change in routes travelled. The final report is sorted from largest decline to largest growth.
def bubblesort(l):
    for a in range(len(l)):
        for b in range(len(l)):
            if l[a][0]<l[b][0]:
                temp=l[a]
                l[a]=l[b]
                l[b]=temp
    return l
import csv
l=[]
resultsfile=open("routegrowthresults.txt", "w")
totals=[]
for i in range(266):
    l.append([])
    for j in range(266):
        l[i].append([0, 0])
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
            l[int(row[7])][int(row[8])][i-startyear]+=1
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
            l[int(row[5])][int(row[6])][i-startyear]+=1
            count+=1
        except:
            print(row)
    print("parsed green "+str(i))
    y.close()
    g.close()
    totals.append(count)
results=[]
for i in range (266):
    for j in range(266):
        if(l[i][j][1]>50):
            try:
                results.append([l[i][j][1]/(l[i][j][0]), "Trips from "+str(i)+" to "+str(j)+" progressed "+str(l[i][j])])
            except:
                results.append([99999999, "Trips from "+str(i)+" to "+str(j)+" progressed "+str(l[i][j])])
print("collated "+str(len(results))+" results")
results=bubblesort(results)
print("Sorted")
for line in results:
    resultsfile.write(str(line[1])+"\n")
resultsfile.write("Total trips progressed "+str(totals))
resultsfile.close()