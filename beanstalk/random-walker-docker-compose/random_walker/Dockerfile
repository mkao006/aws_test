############################################################
# Dockerfile to run a Django-based web application
# Based on an Ubuntu Image
############################################################

## Set the base image to use to Ubuntu
FROM ubuntu:14.04

## Set the file maintainer (your name - the file's author)
MAINTAINER Michal Kao

## Set env variables used in this Dockerfile (add a unique prefix,
## such as RANDOM_WALKER)

# Local directory with project source
ENV RANDOM_WALKER_SRC=.
# Directory in container for all project files
ENV RANDOM_WALKER_SRVHOME=/srv
# Directory in container for project source files
ENV RANDOM_WALKER_SRVPROJ=/srv/random_walker

## Update the default application repository sources list
RUN apt-get update
RUN apt-get install -y \
    python \
    python-pip \
    python-setuptools

## The following is necessary for python to run psycopg2 and postgresql
RUN apt-key adv --keyserver keyserver.ubuntu.com\
     --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" >\
     /etc/apt/sources.list.d/pgdg.list
RUN apt-get update && apt-get -y -q install \
    python-software-properties \
    software-properties-common \
    && apt-get -y -q install \
    postgresql-9.3 \
    postgresql-client-9.3 \
    postgresql-contrib-9.3\
    libpq-dev \
    python-dev \
    python-psycopg2


## The following is necessary for Pillow
RUN sudo apt-get build-dep -y python-imaging
RUN sudo apt-get install -y\
    libjpeg62 \
    libjpeg62-dev

## Create application subdirectories
WORKDIR $RANDOM_WALKER_SRVHOME
RUN mkdir media static logs
VOLUME ["$RANDOM_WALKER_SRVHOME/media/", "$RANDOM_WALKER_SRVHOME/logs/"]

## Copy application source code to SRCDIR
COPY $RANDOM_WALKER_SRC $RANDOM_WALKER_SRVPROJ

## Install Python dependencies
RUN pip install -r $RANDOM_WALKER_SRVPROJ/requirements.txt

## Port to expose
EXPOSE 8000