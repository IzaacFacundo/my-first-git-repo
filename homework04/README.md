# ISS Tracker

The primary objective of this project was to take the position and velocity data provided on the ISS website and  
return various forms of it to the user via a Flask application. In this folder you will find the python script:  
iss\_tracker.py. When run, this code creates an API that can be accessed to return various information about the state  
of the ISS.

## iss\_tracker.py

This python script runs the API that the user can pull from. It has the following routes:
    '\_'
    '\_epochs'
    '\_epochs\_\<epoch>'
    '\_epochs\_\<epoch>\_speed'

### '\_'

'\_' returns the entire data set for the ISS tracker in .xml form. It returns it to the user as a dictionary.

### '\_epochs'

'\_epochs' returns a list of strings that contains all of the epochs (times) contained in the data.

### '\_epochs\_\<epoch>'

'\_epochs\_\<epoch>' returns the state vector of the ISS at the given epoch.

### '\_epochs\_\<epoch>\_speed'

'\_epochs\_\<epoch>\_speed' returns the absolute speed of the ISS in km/s at the given epoch.

## How to run the code

To run the code, you need to run the following command:

`flask --app iss_tracker --debug run`

This will set up the API. Now you can access it via the 'curl' command. Now to access the data, use the command:

`curl localhost:5000[insert route here]`

An example command would be:

`curl localhost:5000/epochs` 
