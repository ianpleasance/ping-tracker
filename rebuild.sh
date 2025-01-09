#!/bin/bash

docker stop pingtracker >/dev/null 2>&1
docker rm pingtracker >/dev/null 2>&1
docker build -t ping-tracker .
docker run -d -p 12345:12345 --name pingtracker ping-tracker
docker logs pingtracker 

