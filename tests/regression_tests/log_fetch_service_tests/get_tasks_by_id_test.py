import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

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
@pytest.mark.usefixtures("run_time_counter", "get_uploaded_task")
@pytest.mark.regression
@pytest.mark.regression_log_fetch
class TestGetTasksById(object):

    @automation_logger(logger)
    def test_get_tasks_by_id_method_works(self, get_uploaded_task):
        allure.step("Verify that response is not empty and status code is 200")
        task_id = get_uploaded_task['taskid']
        _response = ApiClient().log_fetch_svc.get_tasks_by_id(task_id)

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_tasks_by_id_method(self, get_uploaded_task):
        allure.step("Verify response properties and that 'tasks' is list object.")
        task_id = get_uploaded_task['taskid']
        _response = ApiClient().log_fetch_svc.get_tasks_by_id(task_id)[0]

        assert "Do the current tasks" in _response

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_get_tasks_by_id_negative(self, get_uploaded_task):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        task_id = get_uploaded_task['taskid']
        api_.reporting_svc.headers.pop("Authorization")
        _response = api_.log_fetch_svc.get_tasks_by_id(task_id)

        assert isinstance(_response[0], dict)
        assert "name" and "message" and "code" and "status" and "inner" in _response[0].keys()
        assert _response[0]['code'] == "credentials_required"
        assert _response[0]['message'] == "No authorization token was found"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
