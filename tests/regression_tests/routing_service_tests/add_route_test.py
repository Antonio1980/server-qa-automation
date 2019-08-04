import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.entities.location import Location
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("ADD ROUTE")
@allure.description("""
    Functional tests.
    1. Check that service is responded on "routeMe" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/routing_service_tests/add_route_test.py",
                 "TestAddRoute")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_routing
class TestAddRoute(object):

    location = Location()

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_add_route_method_works(self):
        response_ = ApiClient().routing_svc.add_route_v4(self.location)

        assert response_[0] is not None
        assert response_[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_properties_in_add_route_method(self):
        response_ = ApiClient().routing_svc.add_route_v4(self.location)[0]

        assert "url" and "ip" and "port" and "minPort" and "maxPort" and "name" and "countByType" in response_.keys()
        assert  response_["ip"] is not None
        assert  response_["name"] is not None
        assert isinstance(response_["countByType"], dict)

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")
