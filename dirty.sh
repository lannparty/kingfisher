#!/bin/bash

IMAGE=192e9823b613
TARGETS="USLM JOUT OFLX WINA BFC"
DATE=`date +%F-%H-%M-%S`

cat << EOF >> docker-compose.yaml
version: "3"
services:
EOF

for TARGET in ${TARGETS}
do
cat << EOF >> docker-compose.yaml
  ${TARGET}-buy_first-${DATE}:
    image: ${IMAGE}
    container_name: ${TARGET}-buy_first-${DATE}
    network_mode: host
    environment:
    - KINGFISHER_TARGET=${TARGET}
    - KINGFISHER_CLIENT_ID=\${CLIENT_ID}
    - KINGFISHER_STRATEGY=buy_first
  ${TARGET}-sell_first-${DATE}:
    image: ${IMAGE}
    container_name: ${TARGET}-sell_first-${DATE}
    network_mode: host
    environment:
    - KINGFISHER_TARGET=${TARGET}
    - KINGFISHER_CLIENT_ID=\${CLIENT_ID}
    - KINGFISHER_STRATEGY=sell_first
EOF
done

counter=1
cat docker-compose.yaml |grep '${CLIENT_ID}' > /dev/null
until [ $? -eq 1 ]
do
  sed -i 0,/\${CLIENT_ID}/s//$counter/ docker-compose.yaml
  counter=$((counter+1))
  cat docker-compose.yaml |grep '${CLIENT_ID}' > /dev/null
done

docker-compose up -d
rm docker-compose.yaml
