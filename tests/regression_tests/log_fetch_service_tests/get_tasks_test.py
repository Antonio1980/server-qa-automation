import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("GET TASKS")
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetTasks" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/log_fetch_service_tests/get_tasks_test.py",
                 "TestGetTasks")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_log_fetch
class TestGetTasks(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_get_tasks_method_works(self):
        _response = ApiClient().log_fetch_svc.get_tasks()

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties and that 'tasks' is list object.")
    def test_attributes_in_get_tasks_method(self):
        _response = ApiClient().log_fetch_svc.get_tasks()[0]

        assert isinstance(_response, dict)
        assert "tasks" in _response.keys()
        assert isinstance(_response["tasks"], list)
        assert len(_response["tasks"]) > 0

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
