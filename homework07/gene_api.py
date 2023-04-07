#!/usr/bin/env python

import redis
import json
import requests
from flask import Flask

app = Flask(__name__)

rd = redis.Redis(host='10.233.38.133',port=6379,db=0)

@app.route('/data',methods=['POST'])
def post_data_to_redis():
    '''
        This route takes data from the web and uploads it to the running redis database.
        
        Args:
            NONE
        Returns:
            Message confirming behaviour (str)
    '''
    print("This process may take a while\n")
    
    try:
        HGNC_data = requests.get(url='https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
        HGNC_data = HGNC_data.json()['response']['docs'] # narrowed down list of dicts
        rd.set('HGNC_data', json.dumps(HGNC_data))

        return "Successfully loaded gene data into database\n"
    except:
        return "Data post unsuccessful\n"

@app.route('/data',methods=['GET'])
def get_data_from_redis() -> list:
    '''
        This route returns a json list of dicts of the data previously posted to the redis database.

        Args:
            NONE
        Returns:
            data (list): List of dicts containing json data previously posted to the redis database.
    '''
    try:
        data = json.loads(rd.get('HGNC_data'))
    except:
        return("Data could not be retrieved. Make sure data has been posted with the 'POST' method of the /data route.\n")
    return(data)

@app.route('/data',methods=['DELETE'])
def delete_redis_data():
    '''
        This route deletes the data previously posted to the redis database.

        Args:
            NONE
        Returns:
            Success message
    '''
    try:
        rd.delete('HGNC_data')    
        return "Data was succesfully deleted\n"
    except:
        return "Data deletion unsuccessful\n"

@app.route('/genes',methods=['GET'])
def return_gene_ids() -> list:
    '''
        This route parses through the json list of genes and pulls the hgnc_id of each. Then it puts them
        into a list and returns it to the user.

        Args:
            NONE
        Returns:
            hgnc_id_list (list): List of all hgnc_id's in database
    '''
    try:
        HGNC_data = json.loads(rd.get('HGNC_data'))
    except:
        return("Data could not be retrieved. Make sure data has been posted with the 'POST' method of the /data route.\n")
    hgnc_id_list = []
    for item in HGNC_data:
        hgnc_id_list.append(item['hgnc_id'])

    return hgnc_id_list
    

@app.route('/genes/<string:hgnc_id>',methods=['GET'])
def get_specific_data(hgnc_id:str) -> dict:    
    '''
        This route returns all of the data for a specific gene id.
    
        Args:
            hgnc_id (str) : String that contains the hgnc_id for a specific gene
    '''
    try:    
        HGNC_data = json.loads(rd.get('HGNC_data'))
    except:
        return("Data could not be retrieved. Make sure data has been posted with the 'POST' method of the /data route.\n")
    for item in HGNC_data:
        if item['hgnc_id'] == hgnc_id:
            return item
    return('hgnc_id not found.\n')    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

