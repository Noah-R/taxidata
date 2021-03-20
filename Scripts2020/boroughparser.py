import csv
def getZones():
    zonefile=open("taxi_zone_lookup.csv")
    zonereader=csv.reader(zonefile)
    zones=[]
    for row in zonereader:
        if(row[3]=="Boro Zone" or row[3]=="Yellow Zone" or row[3]=="EWR" or row[3]=="Airports" or row[3]=="N/A"):
            zones.append([int(row[0]),row[1]])
    return zones
def getBoroughs():
    return ["EWR", "Bronx", "Manhattan", "Brooklyn", "Queens", "Staten Island", "Unknown"]
def getCombinations():
    boroughs=getBoroughs()
    combs=[]
    for start in range(6):
        combs.append([])
        for end in range(6):
            combs[start].append(boroughs[start]+" to "+boroughs[end])
    return combs
    
#tester code below
#zones=getZones()
#for zone in zones:
#    print(str(zone[0])+" is in "+str(zone[1]))