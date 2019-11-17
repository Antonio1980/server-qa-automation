import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = "GET SYNC ACCESS"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetSyncAccess" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.usefixtures("run_time_counter", )
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/message_sync_service_tests/get_sync_access_test.py",
                 "TestGetSyncAccess")
@pytest.mark.regression
@pytest.mark.regression_message_sync
class TestGetSyncAccess:

    @automation_logger(logger)
    def test_get_sync_access_method_works(self, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.messages_sync_svc.get_sync_access()

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_sync_access_method(self, api_client):
        allure.step("Verify response properties and that 'response' is list object.")
        _response = api_client.messages_sync_svc.get_sync_access()[0]

        assert isinstance(_response, list)
        for item in _response:
            assert item["status"] == "200 OK"

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
