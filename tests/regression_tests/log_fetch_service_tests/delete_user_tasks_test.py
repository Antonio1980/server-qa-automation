import allure
import pytest
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.instruments.api_client import ApiClient
from src.base.utils.log_decorator import automation_logger

test_case = "DELETE USER TASKS"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "DeleteUserTasks" request properly.
    2. Check that service response contains desired properties.
    3. Negative: Check that without authorization it forbidden.
    4. Check that service able to delete 1000 messages.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/log_fetch_service_tests/delete_user_tasks_test.py",
                 "TestDeleteUserTasks")
@pytest.mark.regression
@pytest.mark.regression_log_fetch
class TestDeleteUserTasks:

    @automation_logger(logger)
    def test_delete_user_tasks_method_works(self, api_client, new_task):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.log_fetch_svc.delete_user_tasks(new_task["userid"])

        assert _response[0] is not None
        assert _response[1].status_code == 200
        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_delete_user_tasks_method(self, api_client, new_task):
        allure.step("Verify response properties and that 'response' is list object.")
        _response = api_client.log_fetch_svc.delete_user_tasks(new_task["userid"])[0]

        assert isinstance(_response, dict)
        assert "deletedCount" in _response.keys()

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_delete_user_tasks_negative(self):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        _response = api_.log_fetch_svc.delete_user_tasks("server-qa-automation")

        assert isinstance(_response[0], dict)
        assert "name" and "message" and "code" and "status" and "inner" in _response[0].keys()
        assert _response[0]['code'] == "credentials_required"
        assert _response[0]['message'] == "No authorization token was found"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")

    @pytest.mark.skip #ANTONTODO - reinstate this test when it runs faster
    @automation_logger(logger)
    def test_delete_1000_messages(self, api_client):
        allure.step("Verify that service able to delete 1000 messages.")
        for i in range(1000):
            api_client.log_fetch_svc.add_task("server-qa-automation")

        _response = api_client.log_fetch_svc.delete_user_tasks("server-qa-automation")[0]

        assert _response["deletedCount"] == 1000

        logger.logger.info(F"============ TEST CASE {test_case} / 4 PASSED ===========")
