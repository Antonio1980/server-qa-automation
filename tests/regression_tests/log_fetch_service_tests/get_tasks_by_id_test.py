import json

import allure
import pytest
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.instruments.api_client import ApiClient
from src.base.utils.log_decorator import automation_logger

test_case = "GET TASKS BY ID"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetTasksById" request properly.
    2. Check that service response contains desired properties.
    3. Negative: Check that without authorization it forbidden.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/log_fetch_service_tests/get_tasks_by_id_test.py",
                 "TestGetTasksById")
@pytest.mark.regression
@pytest.mark.regression_log_fetch
class TestGetTasksById:

    @automation_logger(logger)
    def test_get_tasks_by_id_method_works(self, get_uploaded_task, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        task_id = get_uploaded_task['taskid']
        _response = api_client.log_fetch_svc.get_file_by_task_id(task_id)

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_tasks_by_id_method(self, get_uploaded_task, api_client):
        allure.step("Verify response properties and that 'tasks' is list object.")
        task_id = get_uploaded_task['taskid']
        _response = api_client.log_fetch_svc.get_file_by_task_id(task_id)[0]

        assert "Test QA" in _response

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_get_tasks_by_id_negative(self, get_uploaded_task):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        task_id = get_uploaded_task['taskid']
        _response = api_.log_fetch_svc.get_file_by_task_id(task_id)
        json_body = json.loads(_response[0])

        assert "name" and "message" and "code" and "status" and "inner" in json_body.keys()
        assert json_body['name'] == "UnauthorizedError"
        assert json_body['code'] == "credentials_required"
        assert json_body['message'] == "No authorization token was found"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
