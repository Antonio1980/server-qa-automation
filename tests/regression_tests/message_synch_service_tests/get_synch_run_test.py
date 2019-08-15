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
        assert "processTime" and "logFetchRes" and "remoteConfigRes" in response_.keys()
        assert isinstance(response_["logFetchRes"], dict)
        assert "action" and "status" and "data" in response_["logFetchRes"].keys()
        assert "deletedMessages" and "newMessages" and "errors" in response_["logFetchRes"]["data"].keys()
        assert isinstance(response_["logFetchRes"]["data"]["deletedMessages"], list) and \
            isinstance(response_["logFetchRes"]["data"]["newMessages"], list)
        assert "action" and "status" and "data" in response_['remoteConfigRes'].keys()
        assert "newMsg" in response_["remoteConfigRes"]["data"].keys()
        assert "_id" and "type" and "userid" and "data" and "distributionType" in response_["remoteConfigRes"]["data"]["newMsg"].keys()
        assert isinstance(response_["remoteConfigRes"]["data"]["newMsg"]["data"], dict)
        assert "hash" in response_["remoteConfigRes"]["data"]["newMsg"]["data"].keys()

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
