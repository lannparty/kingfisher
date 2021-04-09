#!/bin/bash

IMAGE=192e9823b613

docker stop $(docker ps -a -q)

for i in `seq 1 20`
do
docker run -d --network=host \
  -e KINGFISHER_CLEANING_MODE=True \
  -e KINGFISHER_CLIENT_ID=$i \
  $IMAGE
done
