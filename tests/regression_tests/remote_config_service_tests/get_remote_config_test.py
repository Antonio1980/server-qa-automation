import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("GET REMOTE CONFIG")
@allure.description("""
    Functional test.
    1. Check that service is responded on "GetRemoteConfig" request properly.
    2. Check that service response contains desired properties.
    """)
@pytest.mark.usefixtures("run_time_counter")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/remote_config_service_tests/get_remote_config_test.py",
                 "TestGetRemoteConfig")
@pytest.mark.regression
@pytest.mark.regression_remote_config
class TestGetRemoteConfig(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_get_remote_config_method_works(self):
        _response = ApiClient().remote_config_svc.get_config()

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties and that 'data' is dict object.")
    def test_attributes_in_get_remote_config(self):
        _response = ApiClient().remote_config_svc.get_config()[0]

        assert "_id" and "hash" and "data" and "last_updated" in _response.keys()
        assert isinstance(_response["data"], dict)
        assert "swagger" and "param1" and "param2" and "param3" in _response["data"].keys()

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
