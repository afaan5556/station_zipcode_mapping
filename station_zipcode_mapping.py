import numpy as np
import pandas as pd
from geopy.distance import vincenty

# The csv file of TMY header info from the TMY_Mapping script
mapped_stations_file = 'Mapped_Stations.txt'
# The csv file of station ID's and lat-lon coordinates
mapped_zipcodes_file = 'Mapped_Zip_Codes.txt'
# The headers for the csv file (Since not set up in the TMY_Mapping script)
csv_columns = ['Station_ID', 'Station_Name', 'State', 'Time_Zone', 'Lat', 'Lon', 'Elevation']

# Read in csv file as a df
mapped_stations = pd.read_csv(mapped_stations_file, header = None, names = csv_columns)
# Read in excel file as a df. Convert zip codes to strings so leading zeros are not dropped
mapped_zipcodes = pd.read_csv(mapped_zipcodes_file, converters={'Zip':str})

# Get zipcode from user
user_zip_input = input("Enter the Zip Code: ")

# Function that takes user entered zip code and returns the zip code centroid lat-lon
def get_zip_centroid(zip_df, zip_code=int):
	#1 Convert the zipcode argument into a string so that leading zeros are not dropped
	zip_code = str(zip_code)
	#2 Locate the row in the dataframe that matches the user entered zipcode
	centroid_coordinates = zip_df.loc[zip_df["Zip"] == zip_code]
	#3 Create a tuple that has floats for lat and lon based on the retrieved df row
	# Conversion to float necessary for further use of the resulting data
	centroid_tuple = (float(centroid_coordinates['Lat']), float(centroid_coordinates['Lon']))
	return centroid_tuple

# Function that takes a pair or lat-lon pairs and calcs the Vincenty distance
def calc_dist(zip_centroid, station_coordinates):
	dist = vincenty(zip_centroid, station_coordinates)
	# Convert to float (miles) instead of class<vincenty> object that can not be used later
	dist = dist.miles 
	return dist

def apply_calc_dist(df_mapped_stations, centroid):
	# Create a new column in the df that combines the lat and lon into a column of tuples
	df_mapped_stations['Sation_Coordinates'] = list(zip(df_mapped_stations['Lat'], df_mapped_stations['Lon']))
	# Create a new column in the df that sets for all rows the coordinates returned from the user entered Zip code 
	df_mapped_stations['Zip_Centroid'] = [centroid] * len(df_mapped_stations)
	# Call the calc_dist function on each df entry and vectorize the result to a new column 
	df_mapped_stations['Dist_to_Centroid'] = np.vectorize(calc_dist)(df_mapped_stations['Zip_Centroid'], df_mapped_stations['Sation_Coordinates'])


def get_min_dist(df_mapped_stations):
	min_dist = df_mapped_stations['Dist_to_Centroid'].min()
	min_dist_station = df_mapped_stations.loc[df_mapped_stations['Dist_to_Centroid'] == min_dist]
	return min_dist_station

# Call the get_zip_centroid function on the mapped_zipcodes and the user entered zip code
zip_centroid_tuple = get_zip_centroid(mapped_zipcodes, user_zip_input)

# Call the apply_calc_dist function
apply_calc_dist(mapped_stations, zip_centroid_tuple)

# Call the get_min_dist function to return the closest station to the user entered zip file
return_station = get_min_dist(mapped_stations)
print("The closest weather station is: ", return_station.loc[:, :'Lon'])