import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("UPLOAD FILE TASK")
@allure.description("""
    Functional tests.
    1. Check that service is responded on "UploadFileTasks" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/log_fetch_service_tests/upload_file_task_test.py",
                 "TestUploadFileTask")
@pytest.mark.usefixtures("run_time_count", "task")
@pytest.mark.regression
@pytest.mark.log_fetch_service
class TestUploadFileTask(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_upload_file_task_method_works(self, task):
        task_id = task["taskid"]
        response_ = ApiClient().log_fetch_svc.upload_file_task(task_id, " Do the current tasks")
        assert response_[0] is not None
        assert response_[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response property - updated")
    def test_attributes_in_upload_file_task_method(self, task):
        task_id = task["taskid"]
        response_ = ApiClient().log_fetch_svc.upload_file_task(task_id, " Do the current tasks")[0]
        assert "updated" in response_.keys()
        assert response_["updated"] == "updated"

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
