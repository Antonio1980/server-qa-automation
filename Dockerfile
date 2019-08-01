FROM python:3.7-alpine3.8

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.8/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.8/community" >> /etc/apk/repositories

# upgrade and update VM
RUN apk upgrade
RUN apk update && apk add \
  bash openssh vim curl   \
  build-base git          \
  gcc libxslt-dev         \
  --no-cache ca-certificates

FROM python:3.7

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# install pip
RUN curl -O https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install --upgrade pip

# copy source code
COPY . project
# delete python cache
RUN find project/ -name \*.pyc -delete
# check location
RUN pwd && ls -la

# install virtual environment and requirements
RUN pip install virtualenv
RUN virtualenv venv
RUN pip install -r project/requirements.txt

# Leave it on
CMD tail -f /dev/null