import allure
import pytest
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.utils.log_decorator import automation_logger

test_case = "UPLOAD FILE TASK"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "UploadFileTasks" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/log_fetch_service_tests/upload_file_task_test.py",
                 "TestUploadFileTask")
@pytest.mark.regression
@pytest.mark.regression_log_fetch
@pytest.mark.client
class TestUploadFileTask:

    @automation_logger(logger)
    def test_upload_file_task_method_works(self, get_task, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        task_id = get_task["taskid"]
        _response = api_client.log_fetch_svc.upload_file_task(task_id, " Do the current tasks")

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_upload_file_task_method(self, get_task, api_client):
        allure.step("Verify response property - updated")
        task_id = get_task["taskid"]
        _response = api_client.log_fetch_svc.upload_file_task(task_id, " Do the current tasks")[0]

        assert isinstance(_response, dict)
        assert "_id" and "status" and "to" and "from" and "userid" and "taskid" and "timestamp" in _response.keys()

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
