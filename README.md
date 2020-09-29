
CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Location
 * Technologies
 * Recommended plugins
 * Requirements
 * Tests
 * Configuration
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
- tox - to isolate or manage virtual environments.
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
* $ pytest -v tests --alluredir=src/allure_results

2 Run tests as a package:
* $ pytest -v tests/regression_tests/message_service_tests --alluredir=src/allure_results

3 Run specific test:
* $ pytest -v tests/regression_tests/message_sync_service_tests/get_sync_run_test.py  --alluredir=src/allure_results

4 Run per test group (regression group as example):
* $ pytest -v tests -m regression --alluredir=src/allure_results

5 Generate temporary allure report:
* $ allure serve src/allure_results
  
6 Generate report:
* $ allure generate src/allure_results -o src/allure_reports --clean
  
7 Open allure report:
* $ allure open src/allure_reports

8 Show pytest fixtures and execution plan:
* $ pytest --collect-only
* $ pytest --fixtures

9 Ignore Not Finished tests (cross project)
* $ pytest -v tests/ --ignore-glob='NF*.py'

10 Run tests under tox and pass environment variable:
* $ ENV=int tox -- -m [GROUP_NAME] --alluredir=../src/allure_results

11 Run tests under tox:
* $ tox -- -m [GROUP_NAME] --alluredir=../src/allure_results

* Test Groups:

1. liveness - Production tests.
2. client - all API methods related to the client (App), without Authorization token.
3. functional - Heavy tests, could be with some DB or additional access (required isolated env.).
4. protobuf - Tests with protobuf.
5. regression - Simple API tests (checks basic functional of the services- smoke/sanity).
6. regression_areas_blacklist
7. regression_log_fetch
8. regression_message
9. regression_message_sync
10. regression_remote_config
11. regression_reporting
12. regression_routing
13. regression_licensing


CONFIGURATION
--------------

Project Configuration:
----------------------
NOTE:
Be careful with allure and pytest plugins because of hell of conflicts, current valid plugin configuration is:
plugins: bdd-3.2.1, xdist-1.31.0, forked-1.1.3, allure-pytest-2.8.6

Protobuf installation:
pip install --no-binary=protobuf protobuf
I guess that before it you need pip uninstall protobuf

Tox documentation:
https://tox.readthedocs.io/en/latest/example/general.html

- Project base configuration stores in staging.cfg (per env) that processes by config_definitions.py -> BaseConfig class.

*  logger = if True will append into ./logs/ with cur timestamp as [timestamp]_automation_test.log
*  cloud = if True due to KIBANA endpoint is different on cloud.

- All imports specified in the requirements.txt file.

* To install all project dependencies run command:
* $ pip install -r requirements.txt

- pytest configuration specified in pytest.ini
! currently using: ignore::DeprecationWarning


MAINTAINERS
-----------

* Anton Shipulin <antons@eyenet-mobile.com> 
