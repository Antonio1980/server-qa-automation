import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("GET CONFIG HASH")
@allure.description("""
    Functional test.
    1. Check that service is responded on "GetConfigHash" request properly.
    2. Check that service response contains desired properties.
    """)
@pytest.mark.usefixtures("run_time_count")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/remote_config_service_tests/get_config_hash_test.py",
                 "TestGetConfigHash")
@pytest.mark.regression
@pytest.mark.remote_config_service
class TestGetConfigHash(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_get_hash_method_works(self):
        _response = ApiClient().remote_config_svc.get_config_hash()

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties and 'currentHash' object.")
    def test_attributes_in_get_hash(self):
        _response = ApiClient().remote_config_svc.get_config_hash()[0]

        assert isinstance(_response, dict)
        assert "currentHash" in _response.keys()
        assert _response["currentHash"] is not None

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
