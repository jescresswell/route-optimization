# route-optimization

This repo solves the vehicle routing problem and was implemented for a large Canadian freight company. We take a manifest of deliveries to be made in a day and produce an set of individual manifests and routes for a fleet of trucks. The algorithms can account for vehicle capacities, and having multiple truck depots to dispatch from.

Conventions - Address file should start with depot (starting/ending point for TSP) first

Geocoded file should be in CSV format with (lat/long/address) with the first row being the header "Latitude,Longitude,Address"

Distance matrix file is in CSV format with row/column indices matching that of geocoded file (row=origin, column=destination)

Dependencies: Graphopper folder assumed to be in same location as dmatrix.jar, with subfolder north-america_canada_ontario-gh

Usage: java -jar dmatrix.jar manifest.csv

produces dmatrix.csv
