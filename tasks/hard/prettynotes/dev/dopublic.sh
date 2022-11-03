#!/bin/bash

unlink app || echo "No link found"
unlink Dockerfile || echo "No link found"
unlink docker-compose.yml || echo "No link found"
ln -s ../deploy/app app && ln -s ../deploy/docker-compose.yml docker-compose.yml && ln -s ../deploy/Dockerfile Dockerfile && zip -r ../public/prettynotes.zip * -x dopublic.sh
