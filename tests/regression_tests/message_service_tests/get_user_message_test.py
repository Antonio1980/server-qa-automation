import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = "GET USER MESSAGE"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "GetUserMessages" request properly.
    2. Check that service response contains desired properties.
    """)
@pytest.mark.usefixtures("run_time_counter")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/message_service_tests/get_user_message_test.py",
                 "TestUserMessage")
@pytest.mark.regression
@pytest.mark.regression_messages
class TestUserMessage(object):

    @automation_logger(logger)
    def test_user_message_method_works(self):
        allure.step("Verify that response is not empty and status code is 200")
        _response = ApiClient().messages_svc.get_user_messages("aaa")

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_user_message_method(self):
        allure.step("Verify response properties and that 'messages' is list object.")
        _response = ApiClient().messages_svc.get_user_messages("aaa")[0]

        assert isinstance(_response, dict)
        assert "messages" in _response.keys()
        assert isinstance(_response["messages"], list)
        assert len(_response["messages"]) > 0

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
