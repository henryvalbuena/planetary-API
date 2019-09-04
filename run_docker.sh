#!/bin/bash
app="flaskapp"
img="flask-web-app"
docker run --name ${app} -v $PWD:/www -p 5000:5000 --env-file .env ${img}
if [ $? == 125 ] 
then
  docker start -i ${app}
else
  exit 0
fi