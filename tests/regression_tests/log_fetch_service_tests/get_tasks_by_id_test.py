import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.automation_error import AutomationError
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("GET TASKS BY ID")
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetTasksById" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/log_fetch_service_tests/get_tasks_by_id_test.py",
                 "TestGetTasksById")
@pytest.mark.usefixtures("run_time_counter", "get_uploaded_task")
@pytest.mark.regression
@pytest.mark.regression_log_fetch
class TestGetTasksById(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_get_tasks_by_id_method_works(self, get_uploaded_task):
        task_id = get_uploaded_task['taskid']
        _response = ApiClient().log_fetch_svc.get_tasks_by_id(task_id)

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties and that 'tasks' is list object.")
    def test_attributes_in_get_tasks_by_id_method(self, get_uploaded_task):
        task_id = get_uploaded_task['taskid']
        _response = ApiClient().log_fetch_svc.get_tasks_by_id(task_id)[0]

        assert "Do the current tasks" in _response

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
