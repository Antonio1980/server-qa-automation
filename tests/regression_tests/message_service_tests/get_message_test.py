import allure
import pytest
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.utils.log_decorator import automation_logger

test_case = "GET MESSAGE"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "GetMessage" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/message_service_tests/get_message_test.py",
                 "TestGetMessage")
@pytest.mark.regression
@pytest.mark.regression_message
class TestGetMessage:

    @automation_logger(logger)
    def test_get_message_method_works(self, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.message_svc.get_messages()

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_message_method(self, api_client):
        allure.step("Verify response properties and that 'messages' is list object.")
        _response = api_client.message_svc.get_messages()[0]

        assert isinstance(_response, dict)
        assert "messagesArray" in _response.keys()
        assert isinstance(_response["messagesArray"], list)
        assert len(_response["messagesArray"]) > 0

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
