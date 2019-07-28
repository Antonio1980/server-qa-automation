import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("GET ENDPOINTS")
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetEndpoints" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/routing_service_tests/get_endpoints_test.py",
                 "TestGetEndpoints")
@pytest.mark.usefixtures("run_time_count")
@pytest.mark.regression
@pytest.mark.routing_service
class TestGetEndpoints(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_get_endpoints_method_works(self):
        response_ = ApiClient().routing_svc.get_endpoints()
        assert response_[0] is not None
        assert response_[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties and that response is list object.")
    def test_attributes_in_get_endpoints_method(self):
        response_ = ApiClient().routing_svc.get_endpoints()[0]
        assert isinstance(response_, list)
        assert len(response_) > 0
        for item in response_:
            assert isinstance(item, dict)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
