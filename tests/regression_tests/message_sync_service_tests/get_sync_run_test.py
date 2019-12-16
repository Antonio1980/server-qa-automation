import allure
import pytest
from src.common.utils import logger
from config_definitions import BaseConfig
from src.common.utils.log_decorator import automation_logger

test_case = "GET SYNC RUN"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetSyncRun" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/message_sync_service_tests/get_sync_run_test.py",
                 "TestGetSyncRun")
@pytest.mark.regression
@pytest.mark.regression_message_sync
class TestGetSyncRun:

    @automation_logger(logger)
    def test_get_sync_run_method_works(self, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.messages_sync_svc.get_sync_run()

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_sync_run_method(self, api_client):
        allure.step("Verify response properties and that 'newMessages' is list object.")
        _response = api_client.messages_sync_svc.get_sync_run()[0]

        assert isinstance(_response, dict)
        assert "processTime" and "logFetchRes" and "remoteConfigRes" in _response.keys()
        assert isinstance(_response["logFetchRes"], dict)
        assert "action" and "status" and "data" in _response["logFetchRes"].keys()
        assert "deletedMessages" and "newMessages" and "errors" in _response["logFetchRes"]["data"].keys()
        assert isinstance(_response["logFetchRes"]["data"]["deletedMessages"], list) and \
            isinstance(_response["logFetchRes"]["data"]["newMessages"], list)
        assert "action" and "status" and "data" in _response['remoteConfigRes'].keys()
        assert "newMsg" in _response["remoteConfigRes"]["data"].keys()
        assert "_id" and "type" and "userid" and "data" and "distributionType" in \
               _response["remoteConfigRes"]["data"]["newMsg"].keys()
        assert isinstance(_response["remoteConfigRes"]["data"]["newMsg"]["data"], dict)
        assert "hash" in _response["remoteConfigRes"]["data"]["newMsg"]["data"].keys()

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
