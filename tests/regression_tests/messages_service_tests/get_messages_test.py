import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = "GET MESSAGES"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "GetMessages" request properly.
    2. Check that service response contains desired properties.
    """)
@pytest.mark.usefixtures("run_time_counter")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/messages_service_tests/get_messages_test.py",
                 "TestGetMessages")
@pytest.mark.regression
@pytest.mark.regression_messages
class TestGetMessages(object):

    @automation_logger(logger)
    def test_get_messages_method_works(self):
        allure.step("Verify that response is not empty and status code is 200")
        _response = ApiClient().messages_svc.get_messages()

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} /1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_messages_method(self):
        allure.step("Verify response properties and that 'messages' is list object.")
        _response = ApiClient().messages_svc.get_messages()[0]

        assert isinstance(_response, dict)
        assert "messagesArray" in _response.keys()
        assert isinstance(_response["messagesArray"], list)
        assert len(_response["messagesArray"]) > 0

        logger.logger.info(F"============ TEST CASE {test_case} /1 PASSED ===========")
