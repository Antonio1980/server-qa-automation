import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = "ADD MESSAGES"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "AddMessages" request properly.
    2. Check that service response contains desired properties.
    """)
@pytest.mark.usefixtures("run_time_counter")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/messages_service_tests/add_messages_test.py",
                 "TestAddMessages")
@pytest.mark.regression
@pytest.mark.regression_messages
class TestAddMessages(object):

    @automation_logger(logger)
    def test_add_messages_method_works(self):
        allure.step("Verify that response is not empty and status code is 200")
        _response = ApiClient().messages_svc.add_messages("anton", "sendLog", "task_id")

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} /1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_add_messages_method(self):
        allure.step("Verify response properties and that 'newMsg' is dict object.")
        _response = ApiClient().messages_svc.add_messages("anton", "sendLog", "task_id")[0]

        assert isinstance(_response, dict)
        assert "newMsg" in _response.keys()
        assert isinstance(_response["newMsg"], dict)

        logger.logger.info(F"============ TEST CASE {test_case} /1 PASSED ===========")
