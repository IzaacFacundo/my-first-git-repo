#!/usr/bin/env python

import math
import xmltodict
import requests
from flask import Flask

app = Flask(__name__)

r = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
all_data = xmltodict.parse(r.content)
state_vector_data = all_data['ndm']['oem']['body']['segment']['data']['stateVector']

@app.route('/',methods=['GET'])
def get_all_data():
    '''
    This function returns to the user a dictionary of the entire .xml file given by the ISS website.

    Args: NONE
    Returns:
        all_data (dict) : .xml from ISS website in dictionary form
    '''
    return all_data

@app.route('/epochs',methods=['GET'])
def get_list_of_epochs():
    '''
    This function returns a list of all epochs (times) that are contained within the ISS tracker .xml file

    Args: NONE
    Returns:
        list_of_epochs (list) : list of strings containing each epoch 
    '''
    list_of_epochs = []
    for item in state_vector_data:
        list_of_epochs.append(item['EPOCH'])
    return list_of_epochs 

@app.route('/epochs/<epoch>',methods=['GET'])
def get_state_vector(epoch):
    '''
    This function returns the state vector of the ISS at an inputted epoch. Units are km and km/s

    Args:
        epoch (str) : The epoch at which the user wants the state vector of the ISS

    Returns:
        state_vector (list) : The state vector of the ISS given as a list of floats [X, Y, Z, X_DOT, Y_DOT, Z_DOT]
    '''
    for i in state_vector_data:
        if i['EPOCH'] == epoch:
            X = float(i['X']['#text'])
            Y = float(i['Y']['#text'])
            Z = float(i['Z']['#text'])
            X_DOT = float(i['X_DOT']['#text'])
            Y_DOT = float(i['Y_DOT']['#text'])
            Z_DOT = float(i['Z_DOT']['#text'])
            state_vector = [X, Y, Z, X_DOT, Y_DOT, Z_DOT]
            return state_vector
    return 'Epoch not found.\n'

@app.route('/epochs/<epoch>/speed',methods=['GET'])
def get_speed(epoch):
    '''
        This function returns the absolute speed of the ISS in km/s at an inputted epoch.

        Args:
            epoch (str) : The epoch a twhich the user wants the absolute speed of the ISS

        Returns:
            speed (float) : The absolute speed of the ISS in km/s 
    '''
    for i in state_vector_data:
        if i['EPOCH'] == epoch:
            X_DOT = float(i['X_DOT']['#text'])
            Y_DOT = float(i['Y_DOT']['#text'])
            Z_DOT = float(i['Z_DOT']['#text'])
            speed = str(math.sqrt(X_DOT**2 + Y_DOT**2 + Z_DOT**2))
            return(speed+'\n')
    return 'Epoch not found. Speed cannot be calculated.\n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
