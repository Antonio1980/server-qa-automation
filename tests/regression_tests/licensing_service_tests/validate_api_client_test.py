import allure
import pytest
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.utils.log_decorator import automation_logger

test_case = "VALIDATE CLIENT"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service responded on 'ValidateClient' request properly.
    2. Check that service response contains desired properties.
    3. Negative: Check that without authorization it forbidden.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/licensing_service_tests/validate_api_client_test.py",
                 "TestValidateClient")
@pytest.mark.regression
@pytest.mark.regression_licensing
@pytest.mark.client
class TestValidateClient:

    @automation_logger(logger)
    def test_validate_client_method_works(self, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.licensing_svc.validate_client("C", "api_id", "client_id")

        assert _response[0] is not None
        assert _response[0]['responseType'] == "VALID"
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_validate_client_method(self, api_client):
        allure.step("Verify response properties and that response is dict.")
        _response = api_client.licensing_svc.validate_client("C", "api_id", "client_id")[0]

        assert isinstance(_response, dict)
        assert "responseType" in _response.keys()
        assert _response["responseType"] == "VALID"

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
