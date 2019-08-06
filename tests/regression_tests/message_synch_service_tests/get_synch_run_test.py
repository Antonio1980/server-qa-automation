import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("GET SYNCH RUN")
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetSynchRun" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/message_synch_service_tests/get_synch_run_test.py",
                 "TestGetSynchRun")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_messages_synch
class TestGetSynchRun(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_get_synch_run_method_works(self):
        response_ = ApiClient().messages_synch_svc.get_synch_run()
        assert response_[0] is not None
        assert response_[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties and that 'newMessages' is list object.")
    def test_attributes_in_get_synch_run_method(self):
        response_ = ApiClient().messages_synch_svc.get_synch_run()[0]
        assert "errors" and "processTime" and "deletedMessages" and "newMessages" in response_.keys()
        assert isinstance(response_["errors"], list) and len(response_["errors"]) == 0
        assert isinstance(response_["newMessages"], list) and len(response_["newMessages"]) > 0

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
