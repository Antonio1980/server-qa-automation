import allure
import pytest
from src.common.utils import logger
from config_definitions import BaseConfig
from src.common.instruments.api_client import ApiClient
from src.common.entities.route import Route
from src.common.utils.log_decorator import automation_logger

test_case = "KEEP ALIVE"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "keepAlive" request properly.
    2. Negative: Check that without authorization it forbidden.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/routing_service_tests/keep_alive_test.py", "TestKeepAlive")
@pytest.mark.regression
@pytest.mark.regression_routing
class TestKeepAlive:

    route = Route().set_route(ip="0.0.0.0", name="QA-Test", priority=1, port_list=[8000, 9000])

    @automation_logger(logger)
    def test_keep_alive_method_works(self, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.routing_svc.keep_alive(self.route)

        assert _response[0] is not None
        assert _response[1].status_code == 200
        assert _response[1].reason == 'Created'

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_keep_alive_negative(self):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        _response = api_.routing_svc.keep_alive(self.route)

        assert isinstance(_response[0], dict)
        assert "timestamp" and "status" and "error" and "message" and "path" in _response[0].keys()
        assert _response[0]['error'] == "Unauthorized"
        assert _response[0]['message'] == "the token received is not valid: No token was provided"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
