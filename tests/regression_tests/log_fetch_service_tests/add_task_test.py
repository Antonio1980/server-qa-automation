import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("ADD TASK")
@allure.description("""
    Functional tests.
    1. Check that service is responded on "AddTask" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/log_fetch_service_tests/add_task_test.py",
                 "TestAddTask")
@pytest.mark.usefixtures("run_time_count")
@pytest.mark.regression
@pytest.mark.log_fetch_service
class TestAddTask(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_add_task_method_works(self):
        response_ = ApiClient().log_fetch_svc.add_task("any_string")
        assert response_[0] is not None
        assert response_[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties and that 'response' is list object.")
    def test_attributes_in_add_task_method(self):
        response_ = ApiClient().log_fetch_svc.add_task("another_any_string")[0]
        assert isinstance(response_, list)
        assert len(response_) > 0

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
