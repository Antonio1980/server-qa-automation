import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("GET SYNCH ACCESS")
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetSynchAccess" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/message_synch_service_tests/get_synch_access_test.py",
                 "TestGetSynchAccess")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_messages_synch
class TestGetSynchAccess(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_get_synch_access_method_works(self):
        response_ = ApiClient().messages_synch_svc.get_synch_access()
        assert response_[0] is not None
        assert response_[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties and that 'response' is list object.")
    def test_attributes_in_get_synch_access_method(self):
        response_ = ApiClient().messages_synch_svc.get_synch_access()[0]
        assert isinstance(response_, list)
        for item in response_:
            assert item["status"] == "200 OK"

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
