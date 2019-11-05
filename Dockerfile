FROM ubuntu:latest

MAINTAINER fnndsc "antons@eyenet-mobile.com"

ENV PATH /usr/local/bin:$PATH

RUN apt-get update                    \
    && apt-get install -y             \
    python3-pip python3-dev           \
    && cd /usr/local/bin              \
    && ln -s /usr/bin/python3 python  \
    && pip3 install --upgrade pip

RUN apt-get update          \
    && apt-get install -y   \
    apt-utils bash vim curl \
    git gcc libxslt-dev

COPY . project

RUN pip install --upgrade pip

RUN pip install -r project/requirements.txt

RUN find project/ -name \*.pyc -delete

# RUN rm -r project/src/repository

RUN pwd && ls -la

VOLUME ["src/repository/allure_result"]

WORKDIR project

CMD tail -f /dev/null
