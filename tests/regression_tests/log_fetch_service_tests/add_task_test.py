import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.automation_error import AutomationError
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
@pytest.mark.regression_log_fetch
class TestAddTask(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_add_task_method_works(self):
        try:
            response_ = ApiClient().log_fetch_svc.add_task("any_string")
        except Exception as e:
            logger.logger.error(F"Error while getting server response: {e}")
            raise AutomationError(e)
        assert response_[0] is not None
        assert response_[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties and that 'response' is list object.")
    def test_attributes_in_add_task_method(self):
        try:
            response_ = ApiClient().log_fetch_svc.add_task("any_string")[0]
        except Exception as e:
            logger.logger.error(F"Error while getting server response: {e}")
            raise AutomationError(e)
        assert isinstance(response_, list)
        assert len(response_) > 0

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
