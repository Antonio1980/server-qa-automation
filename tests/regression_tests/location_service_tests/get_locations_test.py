import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = ""


@pytest.mark.skip
@allure.title("GET LOCATIONS")
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetLocations" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/location_service_tests/get_locations_test.py",
                 "TestGetLocation")
@pytest.mark.usefixtures("run_time_count")
@pytest.mark.regression
@pytest.mark.regression_location
class TestGetLocation(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_get_locations_method_works(self):
        response_ = ApiClient().location_svc.get_locations("aaa")
        assert response_[0] is not None
        assert response_[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties and that 'locations' is list object.")
    def test_attributes_in_get_locations_method(self):
        response_ = ApiClient().location_svc.get_locations("aaa")[0]
        assert "locations" in response_.keys()
        assert isinstance(response_["locations"], list)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
