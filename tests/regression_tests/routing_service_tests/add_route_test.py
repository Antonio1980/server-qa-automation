import allure
import pytest
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.entities.location import Location
from src.base.utils.log_decorator import automation_logger

test_case = "ADD ROUTE"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "routeMe" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/routing_service_tests/add_route_test.py", "TestAddRoute")
@pytest.mark.regression
@pytest.mark.regression_routing
@pytest.mark.client
class TestAddRoute:

    location = Location()

    @automation_logger(logger)
    def test_add_route_method_works(self, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.routing_svc.route_me_v4(self.location)

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_properties_in_add_route_method(self, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.routing_svc.route_me_v4(self.location)[0]

        assert isinstance(_response, dict)
        assert "url" and "ip" and "port" and "minPort" and "maxPort" and "name" and "countByType" in _response.keys()
        assert _response["ip"] is not None, "Failed on ip property"
        assert _response["name"] is not None
        assert isinstance(_response["countByType"], dict)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
