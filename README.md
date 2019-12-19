
CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Location
 * Technologies
 * Recommended plugins
 * Requirements
 * Tests
 * Configuration
 * Tips (Python, Docker, Git, Protobuf)
 * Maintainers

INTRODUCTION
------------

The "server-qa-automation"- automation test project for the back-end side of Eye-net (REST API).

LOCATION
---------

- SSH: git@git-v2x.foresight.com:qa-automation/server-qa-automation.git

TECHNOLOGIES
------------

- pytest - advanced test framework.
- allure-pytest - reporting framework.
- elasticsearch - access to KIBANA DB.
- pymongo - access to Mongo DB.
- requests - HTTP/S requests REST API.
- beautifulsoup4 - work with HTML.

RECOMMENDED PLUGINS
-------------------
- shell scripting - ability to execute shell/bash scripts.
- multirun - ability to run several configurations.
- .gitignore - prevents redundant uploads.
- GitLab - projects integration with remote repo.
- CSV - plugin to support csv files.
- Docker - for docker integration.
- CMD support.
- Python Terminal - terminal in separate window.

REQUIREMENTS
------------

1. PyCharm IDEA installed.
2. Python 3.6 or later installed.
3. Python virtualenvironment installed out of the project and activated.
4. Python interpreter configured.
5. Project requirements installed.
6. Project plugins installed.
7. Allure installed locally to: ~/Allure/bin/allure

TESTS
-----

1 Run all tests:
* $ pytest -v tests --alluredir=src/allure/allure_results

2 Run tests as a package:
* $ pytest -v tests/regression_tests/message_service_tests --alluredir=src/allure/allure_results

3 Run specific test:
* $ pytest -v tests/regression_tests/message_sync_service_tests/get_sync_run_test.py  --alluredir=src/allure/allure_results

4 Run per test group (regression group as example):
* $ pytest -v tests -m regression --alluredir=src/allure/allure_results

5 Generate temporary allure report:
* $ allure serve src/allure_results
  
6 Generate report:
* $ allure generate src/allure/allure_results -o src/allure/allure_reports --clean
  
7 Open allure report:
* $ allure open src/allure_reports

8 Show pytest fixtures and execution plan:
* $ pytest --collect-only
* $ pytest --fixtures

9 Ignore Not Finished tests (cross project)
* $ pytest -v tests/ --ignore-glob='NF*.py'

* Test Groups:

1. liveness
2. functional
3. regression
4. regression_areas_blacklist
5. regression_log_fetch
6. regression_message
7. regression_message_sync
8. regression_remote_config
9. regression_reporting
10. regression_routing


CONFIGURATION
--------------

Project Configuration:
----------------------

- Project base configuration stores in staging.cfg (per env) that processes by config_definitions.py -> BaseConfig class.

*  logger = if True will append into ./logs/ with cur timestamp as [timestamp]_automation_test.log
*  cloud = if True due to KIBANA endpoint is different on cloud.

- All imports specified in the requirements.txt file.

* To install all project dependencies run command:
* $ pip install -r requirements.txt

- pytest configuration specified in pytest.ini
! currently using: ignore::DeprecationWarning


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

- Proto contracts:

https://gitlab.com/cx_group/common/proto_contracts

* Generate python proto:
$ GitLab\protoc-3.6.1-win32\bin\protoc -I=GitLab\proto_contracts\src --python_out=GitLab\proto_contracts\gen      


MAINTAINERS
-----------

* Anton Shipulin <antons@eyenet-mobile.com> 
