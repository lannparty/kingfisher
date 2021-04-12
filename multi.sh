#!/bin/bash

IMAGE=2d0744b8fcda
TARGETS="USLM JOUT OFLX WINA BFC"
DATE=`date +%F-%H-%M-%S`

cat << EOF >> docker-compose.yaml
version: "3"
services:
EOF

for TARGET in ${TARGETS}
do
  for i in `seq 1 2`
  do
    cat << EOF >> docker-compose.yaml
  kingfisher-${TARGET}-\${STRATEGY}-${DATE}:
    image: ${IMAGE}
    container_name: kingfisher-${TARGET}-\${STRATEGY}-${DATE}
    network_mode: host
    environment:
    - KINGFISHER_TARGET=${TARGET}
    - KINGFISHER_CLIENT_ID=\${CLIENT_ID}
    - KINGFISHER_STRATEGY=\${STRATEGY}
EOF
  done
done

counter=1
cat docker-compose.yaml |grep '${CLIENT_ID}' > /dev/null
until [ $? -eq 1 ]
do
  sed -i 0,/\${CLIENT_ID}/s//$counter/ docker-compose.yaml
  counter=$((counter+1))
  cat docker-compose.yaml |grep '${CLIENT_ID}' > /dev/null
done

cat docker-compose.yaml |grep '${STRATEGY}' > /dev/null
until [ $? -eq 1 ] 
do
  for i in `seq 1 2`
  do
    if [ $i -eq 1 ]
    then
      sed -i 0,/\${STRATEGY}/s//buy_first/ docker-compose.yaml
    else
      sed -i 0,/\${STRATEGY}/s//sell_first/ docker-compose.yaml
    fi
  done
  cat docker-compose.yaml |grep '${STRATEGY}' > /dev/null
done

docker-compose up -d
rm docker-compose.yaml
