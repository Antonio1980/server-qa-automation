import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = ""


@pytest.mark.skip
@allure.title("GET LOCATIONS BY ID")
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetLocationsById" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/location_service_tests/get_locations_by_id_test.py",
                 "TestGetLocationById")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_location
class TestGetLocationById(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_get_locations_by_id_method_works(self):
        _response = ApiClient().location_svc.get_locations_by_id("location_id")

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties and that 'locations' is list object.")
    def test_attributes_in_get_locations_by_id_method(self):
        _response = ApiClient().location_svc.get_locations_by_id("location_id")[0]

        assert isinstance(_response, dict)
        assert "locations" in _response.keys()
        assert isinstance(_response["locations"], list)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
