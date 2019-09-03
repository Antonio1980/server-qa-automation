import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.entities.location import Location
from src.common.log_decorator import automation_logger

test_case = "ADD LOCATION HISTORY REPORT"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "postReport" request properly.
    2. Negative: Check that without authorization it forbidden.
    """)
@pytest.mark.usefixtures("run_time_counter")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/reporting_service_tests/add_location_history_report_test.py",
                 "TestAddLocationHistoryReport")
@pytest.mark.regression
@pytest.mark.regression_reporting
class TestAddLocationHistoryReport(object):

    location = Location()

    @automation_logger(logger)
    def test_add_location_history_report_method_works(self):
        allure.step("Verify that status code is 200")
        _response = ApiClient().reporting_svc.location_history_report(self.location)

        assert _response[1].status_code == 200
        assert _response[1].reason == 'OK'

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_add_location_history_report_negative(self):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        api_.reporting_svc.headers.pop("Authorization")
        _response = api_.reporting_svc.location_history_report(self.location)

        assert isinstance(_response[0], dict)
        assert "timestamp" and "status" and "error" and "message" and "path" in _response[0].keys()
        assert _response[0]['error'] == "Unauthorized"
        assert _response[0]['message'] == "the token received is not valid: No token was provided"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
