import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = "GET ENDPOINTS"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetEndpoints" request properly.
    2. Check that service response contains desired properties.
    3. Negative: Check that without authorization it forbidden.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/routing_service_tests/get_endpoints_test.py",
                 "TestGetEndpoints")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_routing
class TestGetEndpoints(object):

    @automation_logger(logger)
    def test_get_endpoints_method_works(self):
        allure.step("Verify that response is not empty and status code is 200")
        _response = ApiClient().routing_svc.get_endpoints()

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_endpoints_method(self):
        allure.step("Verify response properties and that response is list object.")
        _response = ApiClient().routing_svc.get_endpoints()[0]

        assert isinstance(_response, list)
        assert len(_response) > 0
        for item in _response:
            assert isinstance(item, dict)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_get_endpoints_negative(self):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        api_.routing_svc.headers.pop("Authorization")
        _response = api_.routing_svc.get_endpoints()

        assert isinstance(_response[0], dict)
        assert "timestamp" and "status" and "error" and "message" and "path" in _response[0].keys()
        assert _response[0]['error'] == "Unauthorized"
        assert _response[0]['message'] == "the token received is not valid: No token was provided"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
