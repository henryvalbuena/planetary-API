# image
FROM ubuntu:xenial
# run updates and install python3
RUN apt-get update -y && apt-get install -y python3-pip python3-dev
# update pip
RUN pip3 install --upgrade pip
# copy requirements
COPY requirements.txt /www/requirements.txt
# image working directory
WORKDIR /www/src
# install requirements
RUN pip3 install -r /www/requirements.txt
# image entry point
ENTRYPOINT ["python3"]
# run the web server
CMD ["views.py"]
