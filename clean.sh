#!/bin/bash

IMAGE=192e9823b613
NUMBEROFCLIENTS=`cat docker-compose.yaml |grep CLIENT_ID |wc -l`

docker stop $(docker ps -a -q)

for i in `seq 1 $NUMBEROFCLIENTS`
do
docker run -d --network=host \
  -e KINGFISHER_CLEANING_MODE=True \
  -e KINGFISHER_CLIENT_ID=$i \
  $IMAGE
done
