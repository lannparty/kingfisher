#!/bin/bash

IMAGE=192e9823b613
DOCKERLOGDIR=/var/lib/docker/containers

docker stop $(docker ps -a -q)

for i in `seq 1 20`
do
docker run -d --network=host \
  -e KINGFISHER_CLEANING_MODE=True \
  -e KINGFISHER_CLIENT_ID=$i \
  $IMAGE
done

docker ps -a |awk '{print $1, $13}' |tail +2 |while read i
do
  ID=`echo $i |awk '{print $1}'`
  NAME=`echo $i |awk '{print $2}'`
  docker logs $ID > logs/$NAME 2>&1
done

