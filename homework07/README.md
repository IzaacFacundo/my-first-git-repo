# Gene API

The gene API is a flask app package that utilizes containers and redis databases. It contains retrieves  
and analyzes data from https://www.genenames.org/download/archive/. This dataset was created by the Human  
Genome Organization, and it contains a comprehensive set of details for almost every gene in the human  
genome. This app retrieves that data from the web, stores it in a redis database, and makes useful parts  
of that data accessible to the user. This package comes with kubernetes support. More details on that at  
the bottom of this README.

## Contents

This folder contains the following files: gene\_api.py, Dockerfile, docker-compose.yaml, and README.md.  
The python script contains the flask app, and the Dockerfile gives the user the option to containerize  
it locally. The docker-compose.yaml file allows for the the app and redis containers to be run at the  
same time and to communicate with each other. There are 5 .yml files used for the redis and flask app  
containers in kubernetes. Finally, there is the README.

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

## How to use Gene API with Kubernetes

Kubernetes is a container orchestration software. It allows the containers to handle traffic and  
sustain uptime even through crashes. In this package, there are two deployments: one for the flask  
app, and one for the redis database. There are two services that maintain constant IPs for the  
pods, and there is one PVC for the redis database. To get everything running, the user must apply  
each of the .yml files using kubectl. To run the Gene API using k8s, use the following command for  
each file in a k8s environment:  


`kubectl apply -f izaac-test-redis-deployment.yml`

`kubectl apply -f izaac-test-redis-pvc.yml`

`kubectl apply -f izaac-test-redis-servie.yml`

`kubectl apply -f izaac-test-flask-deployment.yml`

`kubectl apply -f izaac-test-flask-service.yml`


Before the app can be used, an IP address must be changed in the gene\_api.py script. The IP address  
that needs to be changed is in line 10, and it needs to be changed to the cluster IP for the redis  
service. To find this IP, run the following command:  

`kubectl get services`

Find the cluster IP for the redis service, then put it after 'host=' in line 10 of the gene\_api.py.  
After the user has done this, they need to rebuild and push the image to docker hub and change the  
image in the flask deployment. To first build and push the new image, the user must run the following  
two commands in an environment with docker installed:  

`docker build -t <dockerhub_username>/gene_api:2.0 .`

`docker push <dockerhub_username>/gene_api:2.0`

The <dockerhub_username> should be replaced with the user's DockerHub username. Next, the user should  
navigate to the izaac-test-flask-deployment.yml file and change line 21 to contain the user's  
DockerHub username instead of izaacfacundo. Finally, the user must reset the deployment by deleting  
the pod. The pod will come back online right after, and the app will be accessible. To delete the pod  
run the following command:

`kubectl delete pods <pod_name>`

The pod name can be found by running:

`kubectl get pods`

Now the app should be up and running!

To use the API, the user must exec into one of the pods. This command can be used:  

`kubectl exec -it <flask pod> -- /bin/bash`

Where <flask pod> is the name of the pod given to the flask app instance. This name can be found by  
using the following command:  

`kubectl get pods`

Once the user is in the bash of the pod, the curl commands detailed in the previous section can be  
run with this new IP:

`curl -X POST izaac-test-flask-service:5000/data`

(replacing localhost with izaac-test-flask-service)
