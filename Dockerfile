FROM ubuntu:latest

MAINTAINER "antons@eyenet-mobile.com"

ENV PATH /usr/local/bin:$PATH

RUN apt-get update                               \
    && apt-get install -y                        \
    python3-pip libpython3.7-dev python3.7-dev   \
    && cd /usr/local/bin                         \
    && ln -s /usr/bin/python3 python

RUN apt-get update          \
    && apt-get install -y   \
    apt-utils bash vim curl \
    git gcc libxslt-dev

COPY . project

RUN pip3 install --upgrade pip
RUN rm -rf $HOME/.cache/pip3/*
RUN pip3 install -r project/requirements.txt
# RUN pip3 uninstall protobuf -y
# RUN pip3 install --no-binary=protobuf protobuf

RUN find project/ -name \*.pyc -delete

RUN pwd && ls -la

VOLUME ["project/src/allure_results"]

WORKDIR project

CMD tail -f /dev/null
