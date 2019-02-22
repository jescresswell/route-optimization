# Some entries in the manifest do not include latitude/longitude data
# We geocode these addresses, lat/lng data used in tsp.py
import geocoder
import pandas as pd
from itertools import groupby
import os
from haversine import haversine
import csv

# Read in only the address and latlng data from manifest data, and list of depot locations

data = pd.read_csv('day_manifest.csv',usecols=(5,7,8,9,10,11,12)).as_matrix()
depots = pd.read_csv('depot_locations.csv',usecols=(1,2,3)).as_matrix()

# Haversine finds distance between (lat,long) points, syntax is:
# h = haversine((depots[0][0],depots[0][1]),(depots[1][0],depots[1][1]))

# Some entries do not have latlng data, for those we geocode
# There are several free geocoding services, here we use Google.
for el in data:
    if el[4] == 0:
        g = geocoder.google(el[0]+' '+el[2]+' '+el[3])
        if g.latlng != []:
            el[4]=g.lat
            el[5]=g.lng

# We want to compare our optimized route to routes the freight company actually used
# Actual routes are given in the /manifests folder (not made public). Create a csv for each manifest
# Each manifest has a unique TripNumber in the original data. Group data by TripNumber
sort=[list(v) for l,v in groupby(sorted(data,key=lambda x:x[6]),lambda x:x[6])]

os.chdir('./manifests/')
# For each TripNumber output a csv
# Manifests do not include start/end depot location
# Assume they start/end at geographically closest depot
for el in sort:
    out = pd.DataFrame([["Latitude","Longitude","Address"]])
    tripnum=el[0][6]
    # Identify the closest depot and add it to top of manifest
    depot_dist = [haversine((en[0],en[1]),(el[0][4],el[0][5]))for en in depots]
    index_min = min(range(len(depot_dist)), key=depot_dist.__getitem__)
    close_depot = pd.DataFrame([depots[index_min]])
    out = out.append(close_depot,ignore_index=True)

    for em in el:

        df=pd.DataFrame([[em[4],em[5], em[0]+' '+em[2]+' '+em[3]+' '+em[1]]])
        out=out.append(df,ignore_index=True)
    out.to_csv(str(tripnum)+'.csv',',',index=False,header=False,quoting=csv.QUOTE_NONNUMERIC)

# Code below puts all data into one csv

# output=pd.DataFrame([["latitude","longitude","address"]])
# for el in data:
#    df=pd.DataFrame([[el[4],el[5],el[0]+' '+el[2]+' '+el[3]+' '+el[1]]])
#    output=output.append(df,ignore_index=True)
# output.to_csv('output.csv',',',index=False,header=False)
    

