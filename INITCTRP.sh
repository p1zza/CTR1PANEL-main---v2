#!/bin/bash

echo "Initial Start service"
cd /home/admin/CTR1PANEL-main---v2

docker-compose build
docker-compose up -d
docker-compose down
docker-compose up -d

echo "Service started"