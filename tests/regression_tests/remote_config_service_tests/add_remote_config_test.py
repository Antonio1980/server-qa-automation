import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = "ADD REMOTE CONFIG"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "AddRemoteConfig" request properly.
    2. Check that service response contains desired properties.
    """)
@pytest.mark.usefixtures("run_time_counter", "remote_config")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/remote_config_service_tests/add_remote_config_test.py",
                 "TestAddRemoteConfig")
@pytest.mark.regression
@pytest.mark.regression_remote_config
class TestAddRemoteConfig(object):

    @automation_logger(logger)
    def test_add_remote_config_method_works(self, remote_config):
        allure.step("Verify that response is not empty and status code is 200")
        _response = ApiClient().remote_config_svc.add_remote_config(remote_config)

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_add_remote_config_method(self, remote_config):
        allure.step("Verify response properties and that 'data' is dict object.")
        _response = ApiClient().remote_config_svc.add_remote_config(remote_config)[0]

        assert isinstance(_response, dict)
        assert "hash" and "data" and "last_updated" in _response.keys()
        assert isinstance(_response["data"], dict)
        assert _response["data"] is not None

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
