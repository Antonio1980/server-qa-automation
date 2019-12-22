import allure
import pytest
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.utils.log_decorator import automation_logger

test_case = "GET LOCATION SERVICES HASH"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "getHash" request properly.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/routing_service_tests/get_location_services_hash_test.py",
                 "TestGetLocationServicesHash")
@pytest.mark.regression
@pytest.mark.regression_routing
class TestGetLocationServicesHash:

    @automation_logger(logger)
    def test_get_location_services_hash_method_works(self, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.routing_svc.get_location_services_hash()

        assert _response[0] is not None
        assert _response[1].status_code == 200
        assert _response[1].reason == 'OK'
        assert isinstance(_response[0], str)

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")
