FROM ubuntu:bionic

RUN apt-get update \
 && apt-get install gnupg -y

RUN echo "deb [arch=amd64] http://repo.sawtooth.me/ubuntu/nightly bionic universe" >> /etc/apt/sources.list \
 && (apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 44FC67F19B2466EA \
 || apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 44FC67F19B2466EA) \
 && apt-get update \
 && apt-get install -y -q --allow-downgrades \
    python3 \
    python3-pip \
    python3-setuptools

RUN apt-get install -y -q --allow-downgrades \
    python3-sawtooth-sdk

RUN pip3 install --upgrade protobuf

RUN mkdir -p /var/log/sawtooth

RUN mkdir -p /project/

COPY . /project/

WORKDIR /project/src

RUN pip3 install -r requirements.txt