import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = "GET TASKS"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetTasks" request properly.
    2. Check that service response contains desired properties.
    3. Negative: Check that without authorization it forbidden.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/log_fetch_service_tests/get_tasks_test.py",
                 "TestGetTasks")
@pytest.mark.regression
@pytest.mark.regression_log_fetch
class TestGetTasks:

    @automation_logger(logger)
    def test_get_tasks_method_works(self, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.log_fetch_svc.get_tasks()

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_tasks_method(self, api_client):
        allure.step("Verify response properties and that 'tasks' is list object.")
        _response = api_client.log_fetch_svc.get_tasks()[0]

        assert isinstance(_response, dict)
        assert "tasks" in _response.keys()
        assert isinstance(_response["tasks"], list)
        assert len(_response["tasks"]) > 0

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_get_task_negative(self):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        _response = api_.log_fetch_svc.get_tasks()

        assert isinstance(_response[0], dict)
        assert "name" and "message" and "code" and "status" and "inner" in _response[0].keys()
        assert _response[0]['code'] == "credentials_required"
        assert _response[0]['message'] == "No authorization token was found"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
