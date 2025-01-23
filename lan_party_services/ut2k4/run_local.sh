#!/bin/bash

# Navigate to the directory containing the docker-compose.yml file
cd "$(dirname "$0")"

docker build --platform linux/amd64 -t local/ut2k4:server .
docker run --platform linux/amd64 -it --rm \
    -p 7777:7777/udp \
    -p 7778:7778/udp \
    -p 7787:7787/udp \
    -p 28902:28902/tcp \
    -p 80:80/tcp \
    local/ut2k4:server
    # -v './lan_party_services/ut2k4/data:/usr/src/ut2004/System' \

