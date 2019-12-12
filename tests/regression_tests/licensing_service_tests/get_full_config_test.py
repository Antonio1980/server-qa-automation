import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = "FULL CONFIG"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service responded on 'GetFullConfig' request properly.
    2. Check that service response contains desired properties.
    3. Negative: Check that without authorization it forbidden.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/licensing_service_tests/get_full_config_test.py",
                 "TestGetFullConfig")
@pytest.mark.regression
@pytest.mark.regression_licensing
class TestGetFullConfig:

    @automation_logger(logger)
    def test_get_full_config_method_works(self, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.licensing_svc.get_full_config()

        assert _response[0] is not None
        assert _response[1].status_code == 200
        assert _response[1].reason == "OK"

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_full_config_method(self, api_client):
        allure.step("Verify response properties and that i")
        _response = api_client.licensing_svc.get_full_config()[0]

        assert isinstance(_response, dict)
        assert "clients" in _response.keys()
        assert isinstance(_response["clients"], list)
        assert len(_response["clients"]) > 0
        assert "name" and "_id" and "apiKeys" in _response["clients"][0].keys()
        assert isinstance(_response["clients"][0]["apiKeys"], list)
        assert len(_response["clients"][0]["apiKeys"]) > 0
        assert "applicationIds" and "_id" and "key" and "quotaWarning" and "quotaError" in \
               _response["clients"][0]["apiKeys"][0].keys()

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_activate_area_negative(self):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        _response = api_.licensing_svc.get_full_config()

        assert isinstance(_response[0], dict)
        assert "name" and "message" and "code" and "status" and "inner" in _response[0].keys()
        assert _response[0]['code'] == "credentials_required"
        assert _response[0]['message'] == "No authorization token was found"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
