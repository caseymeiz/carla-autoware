#!/bin/sh
set x+

# Stop all containers // this might be a bad idea if you have other containers you want to keep running
docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q)

# Start the carla simulator that we will connect to later
docker run -p 2000-2002:2000-2002 --privileged --gpus all --net=host -e DISPLAY=$DISPLAY carlasim/carla:0.9.10.1 /bin/bash ./CarlaUE4.sh > /dev/null 2>&1 &

# build and run autoware docker container
docker build -t carla-autoware -f Dockerfile .
docker run \
    -it --rm \
    --volume=$(pwd)/autoware-contents:/home/autoware/autoware-contents:ro \
    --env="DISPLAY=${DISPLAY}" \
    --privileged \
    --net=host \
    --runtime=nvidia \
    carla-autoware:latest