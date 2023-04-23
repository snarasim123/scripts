FROM mongo:4.2.2

# custom label for the docker image
LABEL version="0.1" maintainer="snarasim"

# use 'RUN' to execute commands in the container's bash terminal
RUN apt-get update -y
RUN apt-get remove mongodb-org -y
RUN apt-get install mongodb -y
RUN mkdir -p ./data/db
RUN service mongodb start -y

# expose MongoDB's default port of 27017
EXPOSE 27017