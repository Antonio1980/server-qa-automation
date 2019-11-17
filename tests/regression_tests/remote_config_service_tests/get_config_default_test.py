import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = "GET REMOTE CONFIG DEFAULT"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "GetRemoteConfig" request properly.
    2. Check that service response contains desired properties.
    """)
@pytest.mark.usefixtures("run_time_counter")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/remote_config_service_tests/get_config_default_test.py",
                 "TestGetRemoteConfigDefault")
@pytest.mark.regression
@pytest.mark.regression_remote_config
class TestGetRemoteConfigDefault(object):

    @automation_logger(logger)
    def test_get_remote_config_method_works(self):
        allure.step("Verify that response is not empty and status code is 200")
        _response = ApiClient().remote_config_svc.get_default_config()

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_remote_config(self):
        allure.step("Verify response properties and that 'data' is dict object.")
        _response = ApiClient().remote_config_svc.get_default_config()[0]

        assert isinstance(_response, dict)
        assert "_id" and "hash" and "data" and "last_updated" in _response.keys()
        assert isinstance(_response["data"], dict)
        assert "messagesPollTimeSeconds" and "versionParams" in _response["data"].keys()
        assert isinstance(_response["data"]["versionParams"], dict)
        assert "iOS" and "android" in _response["data"]["versionParams"].keys()
        assert isinstance(_response["data"]["versionParams"]["iOS"], dict)
        assert "storeURL" and "latestVersion" and "minRunnableVersion" in _response["data"]["versionParams"]["iOS"] \
            .keys()
        assert isinstance(_response["data"]["versionParams"]["android"], dict)
        assert "storeURL" and "latestVersion" and "minRunnableVersion" in _response["data"]["versionParams"]["android"] \
            .keys()

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
