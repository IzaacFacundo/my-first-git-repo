# Gene API

The gene API is a flask app package that utilizes containers and redis databases. It contains retrieves  
and analyzes data from https://www.genenames.org/download/archive/. This dataset was created by the Human  
Genome Organization, and it contains a comprehensive set of details for almost every gene in the human  
genome. This app retrieves that data from the web, stores it in a redis database, and makes useful parts  
of that data accessible to the user.

## Contents

This folder contains the following files: gene\_api.py, Dockerfile, docker-compose.yaml, and README.md.  
The python script contains the flask app, and the Dockerfile gives the user the option to containerize  
it locally. The docker-compose.yaml file allows for the the app and redis containers to be run at the  
same time and to communicate with each other. Finally, the README file provides summary information and  
instructions on how to run the code.

## How to pull image from Docker Hub

If you would like to pull the image of the flask app from Docker Hub, you must run the following command:  

`docker pull izaacfacundo/gene_api:1.0`

## How to build a new image using the Dockerfile

If you would instead like to build the image locally, you can run the following command:

`docker build -t izaacfacundo/gene_api:1.0 .`

## How to launch the containerized app

To fully run the app, simply run the following command:  

`docker-compose up`

This will start up the app and redis containers, thus running the app.

To shut down the app, use ctrl C or run the following command:  

`docker-compose down`

## How to use Gene API

To access any of the routes for the API, you must open a new terminal window and use the 'curl' command.  
Here is a list of all the routes with a few sample inputs and outputs:

/data (methods=['POST','GET','DELETE']) - load, retrieve, or delete gene data on app

/genes (methods=['GET']) - get a list of all the unique hgnc\_ids

/genes/<hgnc_id> (methods=['GET']) - get all data on a specific hgnc\_id

The /data route contains 3 methods. To load the data into the app, you must use the POST method of /data:  

`curl -X POST localhost:5000/data`

The data must be loaded into the app before any other routes will work. The output for the previous  
command would be:

`Successfully loaded gene data into database`  

Another example command is:  

`curl localhost:5000/genes/HGNC:34495`

Output:
`
{
  "_version_": 1762504715035213824,
  "agr": "HGNC:34495",
  "alias_symbol": [
    "LOC374920"
  ],
  "ccds_id": [
    "CCDS74411"
  ],
  "date_approved_reserved": "2008-08-06",
  "date_modified": "2023-01-20",
  ...`
