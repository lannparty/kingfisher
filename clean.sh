#!/bin/bash

IMAGE=2d0744b8fcda
DOCKERLOGDIR=/var/lib/docker/containers

docker stop $(docker ps -a -q)

for i in `seq 1 20`
do
docker run -d --rm --network=host \
  -e KINGFISHER_CLEANING_MODE=True \
  -e KINGFISHER_CLIENT_ID=$i \
  $IMAGE
done

docker ps -a |awk '{print $1, $13}' |tail +2 |grep kingfisher

docker ps -a |awk '{print $1, $13}' |tail +2 |grep kingfisher |while read i
do
  ID=`echo $i |awk '{print $1}'`
  NAME=`echo $i |awk '{print $2}'`
  docker logs $ID > logs/$NAME 2>&1
done

