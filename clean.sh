#!/bin/bash

for i in `seq 1 10`
do
docker run -d --network=host \
  -e KINGFISHER_CLEANING_MODE=True \
  -e KINGFISHER_CLIENT_ID=$i \
  0378c7df6cca 
done
