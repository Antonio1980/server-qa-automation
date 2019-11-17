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
    3. Check that service returned default config if name is not requested.
    4. Check that service returned 404 on not existing config name.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.usefixtures("run_time_counter", )
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/remote_config_service_tests/get_config_hash_test.py",
                 "TestGetConfigHash")
@pytest.mark.regression
@pytest.mark.regression_remote_config
class TestGetConfigHash:

    @automation_logger(logger)
    def test_get_hash_method_works(self, get_config_default_name, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.remote_config_svc.get_remote_config_hash(get_config_default_name)

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_hash(self, get_config_default_name, api_client):
        allure.step("Verify response properties and 'currentHash' object.")
        _response = api_client.remote_config_svc.get_remote_config_hash(get_config_default_name)[0]

        assert isinstance(_response, dict)
        assert "hash" in _response.keys()
        assert isinstance(_response["hash"], dict)
        assert "hash" and "name" in _response["hash"].keys()
        assert _response["hash"]["name"] == "default"

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_get_hash_default(self, api_client):
        allure.step("Verify that default config hash returned when name not given.")
        _response = api_client.remote_config_svc.get_remote_config_hash()

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")

    @automation_logger(logger)
    def test_get_hash_negative(self, api_client):
        allure.step("Verify that service responded with 404.")
        _response = api_client.remote_config_svc.get_remote_config_hash("any_stam")

        assert _response[1].status_code == 404
        assert "message" and "statusCode" in _response[0].keys()
        assert _response[0]["message"] == "no hash found for: any_stam"
        assert _response[0]["statusCode"] == 404

        logger.logger.info(F"============ TEST CASE {test_case} / 4 PASSED ===========")
