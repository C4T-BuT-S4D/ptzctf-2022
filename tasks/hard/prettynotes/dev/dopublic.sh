#!/bin/bash

unlink app || echo "No link found"
ln -s ../deploy/app app && zip -r ../public/prettynotes.zip app