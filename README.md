# routing

Conventions - Address file should start with depot (starting/ending point for TSP) first

Geocoded file should be in CSV format with (lat/long/address) with the first row being the header "Latitude,Longitude,Address"

Distance matrix file is in CSV format with row/column indices matching that of geocoded file (row=origin, column=destination)

Dependencies: Graphopper folder assumed to be in same location as dmatrix.jar, with subfolder north-america_canada_ontario-gh

Usage: java -jar dmatrix.jar manifest.csv

produces dmatrix.csv
