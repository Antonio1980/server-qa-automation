import allure
import pytest
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.instruments.api_client import ApiClient
from src.base.utils.log_decorator import automation_logger

test_case = "DELETE CLIENT"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service responded on 'DeleteClient' request properly.
    2. Check that service response contains desired properties.
    3. Negative: Check that without authorization it forbidden.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/licensing_service_tests/delete_api_client_test.py",
                 "TestDeleteApiClient")
@pytest.mark.regression
@pytest.mark.regression_licensing
class TestDeleteApiClient:

    @automation_logger(logger)
    def test_delete_client_method_works(self, api_client, api_name):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.licensing_svc.delete_client(api_name)

        assert _response[0] is not None
        assert _response[1].status_code == 200
        assert _response[1].reason == "OK"

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_delete_client_method(self, api_client, api_name):
        allure.step("Verify response properties and that i")
        _response = api_client.licensing_svc.delete_client(api_name)[0]

        assert isinstance(_response, dict)
        assert "deletedCount" in _response.keys()
        assert _response["deletedCount"] == 1

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_delete_client_negative(self, api_key, api_name):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        _response = api_.licensing_svc.delete_client(api_name)

        assert isinstance(_response[0], dict)
        assert "name" and "message" and "code" and "status" and "inner" in _response[0].keys()
        assert _response[0]['code'] == "credentials_required"
        assert _response[0]['message'] == "No authorization token was found"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")


