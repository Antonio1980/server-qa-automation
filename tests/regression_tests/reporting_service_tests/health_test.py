import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = "HEALTH REPORTING"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "Health" request properly.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/reporting_service_tests/health_test.py",
                 "TestHealth")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_reporting
class TestHealth(object):

    @automation_logger(logger)
    def test_health_reporting(self):
        allure.step("Verify response status code is 200 and properties of the response.")
        _response = ApiClient().reporting_svc.health()

        assert _response[1].status_code == 200
        assert isinstance(_response[0], dict)
        assert "status" in _response[0].keys()
        assert _response[0]["status"] == "UP"

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
