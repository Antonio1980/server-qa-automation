import allure
import pytest
from src.base.instruments.api_client import ApiClient
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.utils.log_decorator import automation_logger

test_case = "ADD MESSAGE"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "AddMessage" request properly.
    2. Check that service response contains desired properties.
    3. Negative: Check that without authorization it forbidden.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/message_service_tests/add_message_test.py",
                 "TestAddMessage")
@pytest.mark.regression
@pytest.mark.regression_message
class TestAddMessage:

    @automation_logger(logger)
    def test_add_message_method_works(self, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.message_svc.add_messages("server-qa-automation", "sendLog", "task_id")

        assert _response[1].status_code == 200
        assert _response[0] is not None

        resp = api_client.message_svc.delete_user_messages("server-qa-automation")
        assert resp[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_add_message_method(self, api_client):
        allure.step("Verify response properties and that 'newMsg' is dict object.")
        _response = api_client.message_svc.add_messages("server-qa-automation", "sendLog", "task_id")[0]

        resp = api_client.message_svc.delete_user_messages("server-qa-automation")
        assert resp[1].status_code == 200

        assert isinstance(_response, dict)
        assert "newMsg" in _response.keys()
        assert isinstance(_response["newMsg"], dict)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)  # BUG  V2X-1888
    def test_add_message_negative(self):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        _response = api_.message_svc.add_messages("server-qa-automation", "sendLog", "task_id")

        assert isinstance(_response[0], dict)
        assert "name" and "message" and "code" and "status" and "inner" in _response[0].keys()
        assert _response[0]['code'] == "credentials_required"
        assert _response[0]['message'] == "No authorization token was found"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
