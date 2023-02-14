#!/usr/bin/env python3

import json
import requests
import math

def calculate_turbidity(calibration_constant:float, detector_current:float) -> float:
    '''
    This function calculates turbidity given two measurements.
    
    Args:
        calibration_constant (float) : This is the calibration constant given by the turbidity instrument.
        detector_current (float) : This is the detector current given by the turbidity instrument

    Returns:
        turbidity (float) :  This is the calculated turbidity of the water measured
    '''
    
    turbidity = calibration_constant * detector_current
    return(turbidity)

def calculate_minimum_time(current_turbidity:float) -> float:
    '''
    This function calculates the minimum time for the measured water to fall below the safe  
    threshold for turbidity. This method uses exponential decay.

    Args:
        current_turbidity (float) : This is the current turbidity of the water

    Returns:
        time_left (float) : This is the amount of hours before the turbidity of the water falls  
        below the safe threshold.
    '''
    
    turbidity_threshold = 1.0
    decay_factor = 0.02
    time_left = 0

    if (current_turbidity < turbidity_threshold):
        pass # skip calculation		
    else:
        time_left = math.log10(turbidity_threshold / current_turbidity) / math.log10(1 - decay_factor)
    
    return(time_left)

def main():
    data = requests.get(url='https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json')
    data = data.json()
    last_five_entries = data["turbidity_data"][-5:]
    
    # get average of last 5 entries
    total = 0
    for i in range(5):
        total += calculate_turbidity(last_five_entries[i]["calibration_constant"],last_five_entries[i]["detector_current"])
        
    average_turbidity = total / 5

    min_time = calculate_minimum_time(average_turbidity)
    
    print("Average turbidity based on most recent five measurements = ", average_turbidity)
    if min_time == 0:
        print("Info: Turbidity is below threshold for safe use")
    else:
        print("Warning: Turbidity is above threshold for safe use")

    print("Minimum time required to return below a safe threshold = ", min_time)

if __name__ == '__main__':
    main()

