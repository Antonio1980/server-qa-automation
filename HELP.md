TIPS: (Python, Docker, Git, Protobuf)
------------------------------------

Python:  
-------
https://www.python.org/downloads/

* install pip:
$ python get-pip.py

* install virtual environment:
$ pip install virtualenv

* create virtual environment:
$ virtualenv venv --python=python3.7

* activate environment for Windows:
$ venv\Scripts\activate

* activate environment for Unix:
$ source venv/bin/activate

* list all packages installed in the environment:
$ pip freeze

* upgrade pip:  
$ python -m pip install --upgrade pip

Docker:
-------
1 Remove containers: 
* $ docker container prune -f

2 Remove images: 
* $ docker image prune -a -f

3 Build image: 
* $ docker build . --rm -f "Dockerfile" -t [project_name]:latest 

4 Get Docker logs:
* $ docker info

5 Get list of used IP's:
* $ docker network ls

6 Inspect Docker connection:
* $ docker network inspect <contiv-srv-net>

7 Log In to GitLab Registry:
* $ docker login registry.gitlab.com

* Remove by ID:
$ docker network rm

* Docker processes:
$ docker ps

* Docker run container:
$ docker exec -it #containername# bash

* Logs dir:
$ cd /usr/local/zend/var/log

* View logs:
$ tail -f | grep *.log

* Kill all UDP connections (Docker included):
$ lsof -P | grep 'UDP' | awk '{print $2}' | xargs kill -9 

Git:
----
* $ git init

* $ git status

* $ git config --global --list

* $ git config --global user.name ""

* $ git config --global user.email ""

* $ cat ~/.gitconfig

* $ git config --global help.autocorrect 1

* $ git config core.autorlf true/false

PROTOBUF
-------- 

- Download and Installation:

https://github.com/protocolbuffers/protobuf/releases/tag/v3.6.1

in any directory:
$ brew install libtool, automake
$ pip3 install --no-binary=protobuf protobuf

- Plugin:
pull https://github.com/dropbox/mypy-protobuf

from mypy-protobuf/python directory:
$ python3 ./setup.py build  
$ python3 ./setup.py -v install

* Generate python proto:
$ GitLab\protoc-3.6.1-win32\bin\protoc -I=GitLab\proto_contracts\src --python_out=GitLab\proto_contracts\gen   

* Generate mypy proto (with autocomplete and keywords):
$ protoc -I=. --mypy_out=../python_out --python_out=../python_out LocationServiceResponse.proto   
