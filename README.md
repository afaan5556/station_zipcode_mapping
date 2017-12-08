# station_zipcode_mapping
This Python script takes in a user entered zip code and returns the closest weather station using the geopy.distance vincenty function.

## Data required
* A csv file containing TMY file header data
** For example `690150,TWENTYNINE PALMS,CA,-8.0,34.300,-116.167,626`
* A csv file that contains the lat-lon centroid coordinates of all zip-codes
* Both files provided for reference

## Variables
* `csv_columns` is a variable that sets up the column header names for the TMY header data csv file. Only needed if the csv file does not contain column headers. 

## Use
Place the script in the same folder as the csv files.

Running the script in a terminal should take a zip code user input and return the vincenty calculated closest TMY weather station.