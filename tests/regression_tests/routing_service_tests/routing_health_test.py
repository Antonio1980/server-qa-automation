import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = "HEALTH ROUTING"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "Health" request properly.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/routing_service_tests/routing_health_test.py",
                 "TestHealthRouting")
@pytest.mark.regression
@pytest.mark.regression_messages_synch
class TestHealthRouting:

    @automation_logger(logger)
    def test_health_routing(self, api_client):
        allure.step("Verify response status code is 200 and properties of the response.")
        _response = api_client.routing_svc.health()

        assert _response[1].status_code == 200
        assert isinstance(_response[0], dict)
        assert "status" in _response[0].keys()
        assert _response[0]["status"] == "UP"

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
