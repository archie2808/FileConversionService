To run the file converter, ensure docker is installed on the server. 
Then run the following command in the terminal:
```docker compose up -d --build```
This will build and deploy the converter and the file scanning service on docker.
The converter will be available at http://localhost:5000

To conduct load testing load testing on the container, either navigate to the terminal 
inside the docker application or run the following command in the terminal:
```docker exec -it <container_name_or_id> /bin/sh```
Then: 
``locust``
Navigate to http://localhost:8089 to conduct load testing on the converter.

To run nnom and gather resource usage statistics, run:
```nmon``` - to access the interactive nmon interface
```nmon -f -s {interval} -c {count} -F {output_filename}``` - to export data to a .nmon file



