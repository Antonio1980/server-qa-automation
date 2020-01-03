import allure
import pytest
from src.base.lib_ import logger
from src.base.instruments.api_client import ApiClient
from config_definitions import BaseConfig
from src.base.lib_.log_decorator import automation_logger

test_case = "GET REMOTE CONFIG BY NAME"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "GetRemoteConfigByName" request properly.
    2. Check that service response contains desired properties.
    3. Check that service returned 404 on not existing config name.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/remote_config_service_tests/get_config_by_name_test.py",
                 "TestGetRemoteConfigByName")
@pytest.mark.regression
@pytest.mark.regression_remote_config
@pytest.mark.client
class TestGetRemoteConfigByName:

    @automation_logger(logger)
    def test_get_remote_config_by_name_method_works(self, get_config_default_name, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.remote_config_svc.get_config_by_name(get_config_default_name)

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_remote_config_by_name(self, get_config_default_name, api_client):
        allure.step("Verify response properties and that 'data' is dict object.")
        _response = api_client.remote_config_svc.get_config_by_name(get_config_default_name)[0]

        assert isinstance(_response, dict)
        assert "_id" and "hash" and "data" and "last_updated" and "name" and "description" in _response.keys()
        assert isinstance(_response["data"], dict)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_get_remote_config_by_name_negative(self):
        allure.step("Verify that service responded with 404 if config name not exists.")
        _response = ApiClient().remote_config_svc.get_config_by_name("any_stam")

        assert _response[1].status_code == 404
        assert "message" and "statusCode" in _response[0].keys()
        assert _response[0]["message"] == "no config found for: any_stam"
        assert _response[0]["statusCode"] == 404

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
