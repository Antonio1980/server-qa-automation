import allure
import pytest
from src.common.utils import logger
from config_definitions import BaseConfig
from src.common.utils.log_decorator import automation_logger

test_case = "ADD MESSAGE"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "AddMessage" request properly.
    2. Check that service response contains desired properties.
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
        _response = api_client.message_svc.add_messages("anton", "sendLog", "task_id")

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_add_message_method(self, api_client):
        allure.step("Verify response properties and that 'newMsg' is dict object.")
        _response = api_client.message_svc.add_messages("anton", "sendLog", "task_id")[0]

        assert isinstance(_response, dict)
        assert "newMsg" in _response.keys()
        assert isinstance(_response["newMsg"], dict)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
