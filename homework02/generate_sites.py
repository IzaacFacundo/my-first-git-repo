#!/usr/bin/env python3

import json
import random

def get_random_latitude():
	""" 
	This function returns a random float between 16 and 18.
	
	Returns:
		result (float) : random float between 16 and 18
	"""
	result = random.uniform(16,18)
	return(result)

def get_random_longitude():
	""" 
	This function returns a random float between 82 and 84.
	
	Returns:	
		result (float) : random float between 82 and 84
	"""
	result = random.uniform(82,84)
	return(result)

def get_random_composition():
	"""
	This function returns either stony, iron, or stony-iron randomly.
	
	Returns:
		comp (str) : either stony, iron, or stony-iron (strings)

	"""
	rand = random.randint(1,3)
	if rand == 1:
		comp = "stony"
	elif rand == 2:
		comp = "iron"
	elif rand == 3:
		comp = "stony-iron"

	return(comp)
def main():
	sites = [] # create list object
	
	for i in range(1,6): # create 5 sites with customized random data
		sites.append( 
		{
			"site_id": i,
			"latitude": get_random_latitude(),
			"longitude": get_random_longitude(),
			"composition": get_random_composition()
		})
	
	sites = { # format final object into dict of list of dicts
			"sites": sites
		}

	json_sites = json.dumps(sites, indent=None) # Serialize json
	
	with open("site_data","w") as outfile: # Write data to json_sites
		outfile.write(json_sites)

if __name__ == '__main__':
	main()

	
