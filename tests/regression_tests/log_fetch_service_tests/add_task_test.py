import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = "ADD TASK"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "AddTask" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/log_fetch_service_tests/add_task_test.py", "TestAddTask")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_log_fetch
class TestAddTask(object):

    @automation_logger(logger)
    def test_add_task_method_works(self):
        allure.step("Verify that response is not empty and status code is 200")
        _response = ApiClient().log_fetch_svc.add_task("qa_test_qa")

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_add_task_method(self):
        allure.step("Verify response properties and that 'response' is list object.")
        _response = ApiClient().log_fetch_svc.add_task("qa_test_qa")[0]

        assert isinstance(_response, list)
        assert len(_response) > 0

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
