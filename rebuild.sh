#!/bin/bash

docker stop pingtracker 
docker rm pingtracker
docker build -t ping-tracker .
docker run -d -p 12345:12345 --name pingtracker ping-tracker
docker logs pingtracker 

