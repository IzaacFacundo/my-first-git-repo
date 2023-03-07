#!/usr/bin/env python

import math
import xmltodict
import requests
from flask import Flask
from flask import request

app = Flask(__name__)

r = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
all_data = xmltodict.parse(r.content)
state_vector_data = all_data['ndm']['oem']['body']['segment']['data']['stateVector']

@app.route('/',methods=['GET'])
def get_all_data() -> dict:
    '''
    This function returns to the user a dictionary of the entire .xml file given by the ISS website.

    Args: NONE
    Returns:
        all_data (dict) : .xml from ISS website in dictionary form
    '''
    if not all_data:
        return "Error: ISS Data has been deleted. Use route '/post-data' to restore data.\n"

    return all_data

@app.route('/epochs',methods=['GET'])
def get_list_of_epochs() -> dict:
    '''
    This function returns a list of all epochs (times) that are contained within the ISS tracker .xml file

    Args: NONE
    Returns:
        json_list_of_epochs (dict) : list of strings containing each epoch
    '''
    if not all_data:
        return "Error: ISS Data has been deleted. Use route '/post-data' to restore data.\n"

    limit = request.args.get('limit',len(state_vector_data))
    try:
        limit = int(request.args.get('limit',len(state_vector_data)))
    except ValueError:
        return("Invalid limit parameter; limit must be an integer.\n", 400)
    if limit < 0:
        return("Error: limit must be a positive integer.\n")
    # If limit is higher than the number of epochs, we will just give all epochs without error message

    try:
        offset = int(request.args.get('offset',0))
    except ValueError:
        return("Invalid offset parameter; offset must be an integer.\n", 400)
    if offset < 0:
        return("Error: offset must be a positive integer.\n")
    if offset >= len(state_vector_data):
        return("Error: offset is equal to or greater than number of epochs (" + str(len(state_vector_data)) + ").\n")

    list_of_epochs = []
    offset_count = 0
    epoch_count = 0
    for item in state_vector_data:
        if offset_count < offset:
            offset_count += 1
            continue
        if epoch_count == limit:
            break
        list_of_epochs.append(item['EPOCH'])
        epoch_count += 1
    json_list_of_epochs = {'epochs':list_of_epochs}

    return json_list_of_epochs

@app.route('/epochs/<string:epoch>',methods=['GET'])
def get_state_vector(epoch:str) -> dict:
    '''
    This function returns the state vector of the ISS at an inputted epoch. Units are km and km/s

    Args:
        epoch (str) : The epoch at which the user wants the state vector of the ISS

    Returns:
        state_vector (dict) : The state vector of the ISS given as a list of floats [X, Y, Z, X_DOT, Y_DOT, Z_DOT]
    '''
    if not all_data:
        return "Error: ISS Data has been deleted. Use route '/post-data' to restore data.\n"

    for i in state_vector_data:
        if i['EPOCH'] == epoch:
            X = float(i['X']['#text'])
            Y = float(i['Y']['#text'])
            Z = float(i['Z']['#text'])
            X_DOT = float(i['X_DOT']['#text'])
            Y_DOT = float(i['Y_DOT']['#text'])
            Z_DOT = float(i['Z_DOT']['#text'])
            state_vector = [X, Y, Z, X_DOT, Y_DOT, Z_DOT]
            return({"state_vector":state_vector})
    return 'Epoch not found.\n'

@app.route('/epochs/<string:epoch>/speed',methods=['GET'])
def get_speed(epoch:str) -> dict:
    '''
        This function returns the absolute speed of the ISS in km/s at an inputted epoch.

        Args:
            epoch (str) : The epoch a twhich the user wants the absolute speed of the ISS

        Returns:
            speed (str) : The absolute speed of the ISS in km/s
    '''
    if not all_data:
        return "Error: ISS Data has been deleted. Use route '/post-data' to restore data.\n"

    for i in state_vector_data:
        if i['EPOCH'] == epoch:
            X_DOT = float(i['X_DOT']['#text'])
            Y_DOT = float(i['Y_DOT']['#text'])
            Z_DOT = float(i['Z_DOT']['#text'])
            speed = str(math.sqrt(X_DOT**2 + Y_DOT**2 + Z_DOT**2))
            speed = speed
            return({"speed":speed})
    return 'Epoch not found. Speed cannot be calculated.\n'

@app.route('/help',methods=['GET'])
def help_menu() -> str:
    '''
        This function takes no arguments and returns a block of text detailing all of the routes
        a user can call in this flask app.

        Args: NONE

        Returns:
            message (str) : A large, detailed string that details all user commands to this app
    '''
    intro = "Usage (terminal): curl 'localhost:5000[route]' \n\n"
    routes = "Routes: \n"
    slash = "    '/'                        Returns entire ISS dataset in json dictionary form\n"
    epochs = "    '/epochs'                  Returns a list of all epochs of recorded ISS data\n"
    query = "                                   Query Parameters: \n"
    queryl = "                                       limit   Positive integer of how many epochs to display\n"
    queryo = "                                       offset  Positive integer of which epoch will start the list\n"
    state = "    '/epochs/<epoch>'          Returns the state vector (position in km and velocity in km/s) of the \n
                    ISS at a specified epoch\n"
    speed = "    '/epochs/<epoch>/speed'    Returns the absolute speed of specific epoch in km/s\n"
    help_route = "    '/help'                    Returns this help menu\n"
    delete_data = "    '/delete-data'             Deletes all ISS Data stored in app. Must be run with '-X DELETE' \n
                     following the curl command and preceding the address and route.\n"
    post_data = "    '/post-data'               Retrieves ISS data from the ISS website restoring it after use of \n                        '/delete-data'. Must be run with '-X POST' following the curl \n                               command and preceding the address and route.\n"
    message = "\n" + intro + routes + slash + epochs + query + queryl + queryo + state + speed + help_route + delete_data + post_data
    return message

@app.route('/delete-data',methods=['DELETE'])
def delete_all_data() -> str:
    '''
        This function deletes the ISS Data loaded in upon the startup of this flask app. All data
        dictionaries are emptied when this function runs.

        Args: NONE

        Returns: Returns a string saying the ISS Data has been deleted
    '''
    global r, all_data, state_vector_data
    r = {}
    all_data = {}
    state_vector_data = {}
    return "Successfully deleted all ISS Data\n"

@app.route('/post-data',methods=['POST'])
def retrieve_data_again() -> str:
    '''
        This function gets the ISS data back from the ISS website. It gets it using the requests.get
        method. The function fills the dictionaries emptied by the '/delete-data' route.

        Args: NONE

        Returns: Returns a string saying the ISS Data has been deleted
    '''
    global r, all_data, state_vector_data
    r = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    all_data = xmltodict.parse(r.content)
    state_vector_data = all_data['ndm']['oem']['body']['segment']['data']['stateVector']
    return "Restored ISS Data\n"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
