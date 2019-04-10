#!/bin/bash

docker run -p 5000:5000 -v /home/andre/Documents/attempo_docker_files:/server/utils/uploadImages --name tma-attempo-server --rm \
--env HOST=192.168.1.121 --env PORT=5432 --env DBNAME=attempo --env DBUSER=postgres --env DBPASS=postgres \
-d attempo-server:v2
