#!/bin/bash
img="flask-web-app"
docker build -t ${img} .
docker system prune