#!/usr/bin/env python3
import json
import math

START_LAT = 16.
START_LON = 82.
SPEED = 10.
RADIUS = 3389.5

def calc_gcd(latitude_1: float, longitude_1: float, latitude_2: float, longitude_2: float) -> float:
	lat1, lon1, lat2, lon2 = map( math.radians, [latitude_1, longitude_1, latitude_2, longitude_2] )
    
	d_sigma = math.acos( math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(abs(lon1-lon2)))
	return ( RADIUS * d_sigma )

def get_sample_time(composition: str) -> float:
	"""
	This function reads in a key value and calculates a sample time.

	Args:
		composition (str) : The key value related to the composition of a meteorite landing site

	Returns:
		(float) : Returns either 1., 2., or 3. These floats correspond to hours.
	"""
	if composition == "stony":
		return(1.)
	elif composition == "iron":
		return(2.)
	elif composition == "stony-iron":
		return(3.)

def main():
	with open("site_data","r") as f:
		sites = json.load(f)
	legs = [] # initialize to be appended later
	latitudes, longitudes = [START_LAT],[START_LON]
	total_time = 0
	for i in range(5): # create list of lats and lons to make calling them easier
		latitudes.append(sites["sites"][i]["latitude"])
		longitudes.append(sites["sites"][i]["longitude"])

	for i in range(5):
		distance = calc_gcd(latitudes[i],longitudes[i],latitudes[i+1],longitudes[i+1])
		travel_time = distance / SPEED
		sample_time = get_sample_time(sites["sites"][i]["composition"])
		"""
		legs.append({
				"leg": i,
				"time_to_travel": travel_time,
				"time_to_sample": sample_time
			}) 
		"""
		print("leg = ",i+1,", time to travel = ",travel_time," hr, time to sample = ",sample_time," hr")
		total_time += (travel_time + sample_time)
				
	print("=" * 31)
	print("number of legs = 5, total time elapsed = ", total_time, " hr")		
	
	

if __name__ == '__main__':
	main() 
