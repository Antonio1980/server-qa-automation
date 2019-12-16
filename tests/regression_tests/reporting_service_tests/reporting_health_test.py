import allure
import pytest
from src.common.utils import logger
from config_definitions import BaseConfig
from src.common.utils.log_decorator import automation_logger

test_case = "HEALTH REPORTING"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "Health" request properly.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/reporting_service_tests/reporting_health_test.py",
                 "TestHealthReporting")
@pytest.mark.regression
@pytest.mark.regression_reporting
class TestHealthReporting:

    @automation_logger(logger)
    def test_health_reporting(self, api_client):
        allure.step("Verify response status code is 200 and properties of the response.")
        _response = api_client.reporting_svc.health()

        assert _response[1].status_code == 200
        assert isinstance(_response[0], dict)
        assert "status" in _response[0].keys()
        assert _response[0]["status"] == "UP"

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
