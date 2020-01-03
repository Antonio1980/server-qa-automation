import allure
import pytest
from src.base.lib_ import logger
from config_definitions import BaseConfig
from src.base.lib_.log_decorator import automation_logger

test_case = "ADD LOCATION SERVICES HASH"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "addHash" request properly.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/routing_service_tests/add_location_services_hash_test.py",
                 "TestAddLocationServicesHash")
@pytest.mark.regression
@pytest.mark.regression_routing
class TestAddLocationServicesHash:

    @pytest.fixture
    @automation_logger(logger)
    def get_hash(self, api_client):
        _response = api_client.routing_svc.get_location_services_hash()
        assert _response[1].status_code == 200
        return _response[0]

    @automation_logger(logger)
    def test_add_location_services_hash_method_works(self, api_client, get_hash):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.routing_svc.add_location_services_hash(get_hash)

        assert _response[0] is not None
        assert _response[1].status_code == 200
        assert _response[1].reason == 'OK'

        resp = api_client.routing_svc.get_location_services_hash()[0]
        assert resp == get_hash

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")
