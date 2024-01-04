###############
# Build Stage #
###############

FROM python:3.9.13-slim as build

ENV apt_packages_build="\
  build-essential \
  ca-certificates \
  gcc \
  git \
  libpq-dev \
  default-libmysqlclient-dev \
  default-mysql-client \
  python3-dev \
  make \
  libmariadb-dev \
  pkg-config \
  software-properties-common \
  ssh-client \
"

RUN \
	apt update && \
	apt install -y --no-install-recommends \
	${apt_packages_build}

# Setup the app directory
ENV app_dir=/nba_app/
WORKDIR ${app_dir}

RUN python -m venv ./venv
ENV PATH="${app_dir}/venv/bin:$PATH"

# Install the pip dependencies from requirements.txt
COPY requirements.txt .

RUN \
  pip install --upgrade pip wheel && \
  pip install --no-cache-dir -r requirements.txt

##############
# Main Stage #
##############

FROM ubuntu:22.04

LABEL org.opencontainers.image.authors="UA"

# Set apt and TZ options
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London

# Define the username and app directory
ENV conuser=automater
ENV app_dir=/nba_app

ENV apt_packages_main="\
  awscli \
  python3-pip \
"

# Update apt and install required system packages as root
RUN \
  apt update && \
  apt upgrade -y && \
  apt install -y --no-install-recommends ${apt_packages_main} && \
  rm -rf /var/lib/apt/lists/*

# Add the deadsnakes PPA repo and python 3.9
RUN \
  apt update && \
  apt-get install -y default-mysql-client && \
  apt install -y software-properties-common && \
  add-apt-repository ppa:deadsnakes/ppa && \
  apt install -y python3.9 python3.9-venv && \
  apt-get -y update && \ 
  apt-get -y install vim nano && \
  update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

# Create a user to run our app in
RUN useradd -m $conuser -s /bin/bash

# Create and setup the app dir
RUN mkdir $app_dir && chown $conuser:$conuser $app_dir
WORKDIR $app_dir

# There are some issues if the python binaries aren't removed
COPY --from=build --chown=$conuser:$conuser $app_dir/venv ./venv
RUN rm ./venv/bin/python*

# Change context to our app user
USER $conuser

# Create the virtual env as the context user
RUN python -m venv ./venv

# Equivalent of activating the venv
ENV PATH="${app_dir}/venv/bin:$PATH"

# Set the AWS Default Region
ENV AWS_DEFAULT_REGION=eu-west-2

# Copy the python scripts we want in the container
COPY --chown=$conuser:$conuser . .

RUN git clone 

ENTRYPOINT tail -F anything

