# Water Quality Turbidity Tests

The primary objective of this project was to measure and calculate the turbidity of a body  
of water on the surface of Mars and calculate how long it would take to be sufficiently clean.  
In this folder you will find two python scripts: analyze\_water.py and test\_analyze\_water.py.  
Both of these scripts interact together to complete the objective.

## Turbidity Data

The data used for this project can be found here:  
https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity\_data.json
The data is a .json containing a list of dictionaries. The list is updated every hour with  
a new dictionary. The dictionaries contain measurement data from the body of water being measured.  

## analyze\_water.py

analyze\_water.py does exactly that: it analyzes the water. It does this by utilizing two  
functions: calculate-turbidity() and calculate-minimum-time(). The first thing the script does  
is access the turbidity data from Github using the 'requests' library. Then it isolates the  
five most recent entries. Finally, it calculates the average turbidity and time for the water  
to clear and spits out a message detailing its findings. Here is a sample output message:

    Average turbidity based on most recent five measurements = 1.1992 NTU
    Warning: Turbidity is above threshold for safe use
    Minimum time required to return below a safe threshold = 8.99 hours

## test\_analyze\_water.py

This script uses the 'pytest' library to test the functions in analyze\_water.py.

## How to use the code

### How to run the code

To run the code, all you need to do is use the python3 command in your terminal. Run  
analyze\_water.py to analyze the most recent five turbidity measurements and output the  
results.

### How to interpret results

There are two outcomes for results: either the water is below or above the threshold for safe  
use. If it is below, the water is safe for use. If it is above, you must wait at least the  
posted number of hours before it is safe for use.
 
