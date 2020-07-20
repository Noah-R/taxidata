def quicksort(list):
    if(len(list)<2):
        return list
    pivotspot=len(list)-1
    pivot=list[pivotspot][0]
    i=0
    while i<pivotspot:
        if(list[i][0]>=pivot):
            list.append(list.pop(i))
            i-=1
            pivotspot-=1
        i+=1
    return quicksort(list[:pivotspot])+[list[pivotspot]]+quicksort(list[pivotspot+1:])
import csv
y=open("yellow0619.csv")
g=open("green0619.csv")
l=[]
count=0
for i in range(266):
    l.append([])
    for j in range(266):
        l[i].append(0)
readery=csv.reader(y)
for row in readery:
    try:
        #1 for trips
        #row[4] for miles
        #row[16] for dollars
        l[int(row[7])][int(row[8])]+=float(row[4])
        count+=1
    except:
        print(row)
print("parsed yellow")
readerg=csv.reader(g)
for row in readerg:
    try:
        #1 for trips
        #row[8] for miles
        #row[16] for dollars
        l[int(row[5])][int(row[6])]+=float(row[8])
        count+=1
    except:
        print(row)
print("parsed green")
results=[]
for i in range (266):
    for j in range(266):
        if(l[i][j]>1):
            results.append([l[i][j], str(l[i][j])+" units from "+str(i)+" to "+str(j)])
print("collated "+str(len(results))+" results")
results=quicksort(results)
for line in results:
    print(line)
print(str(count)+" total")