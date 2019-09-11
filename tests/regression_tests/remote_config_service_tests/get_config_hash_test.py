import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = "GET CONFIG HASH"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "GetConfigHash" request properly.
    2. Check that service response contains desired properties.
    """)
@pytest.mark.usefixtures("run_time_counter")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/remote_config_service_tests/get_config_hash_test.py",
                 "TestGetConfigHash")
@pytest.mark.regression
@pytest.mark.regression_remote_config
class TestGetConfigHash(object):

    @automation_logger(logger)
    def test_get_hash_method_works(self):
        allure.step("Verify that response is not empty and status code is 200")
        _response = ApiClient().remote_config_svc.get_config_hash()

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_hash(self):
        allure.step("Verify response properties and 'currentHash' object.")
        _response = ApiClient().remote_config_svc.get_config_hash()[0]

        assert isinstance(_response, dict)
        assert "currentHash" in _response.keys()
        assert _response["currentHash"] is not None

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
