import allure
import pytest
from src.common.utils import logger
from src.common.instruments.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.entities.app_client import AppClient
from src.common.entities.report_item import ReportItem
from src.common.utils.log_decorator import automation_logger

test_case = "ADD BULK ANALYTICS REPORT"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "postReport" request properly.
    2. Negative: Check that without authorization it forbidden.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/reporting_service_tests/add_bulk_analytics_report_test.py",
                 "TestAddBulkAnalyticsReport")
@pytest.mark.regression
@pytest.mark.regression_reporting
class TestAddBulkAnalyticsReport:

    client_ = AppClient()
    report_type, session_id = "QaReport", "Test Report"
    report_item = ReportItem(report_type, session_id)

    @automation_logger(logger)
    def test_add_bulk_analytics_report_method_works(self, api_client):
        allure.step("Verify that status code is 201")
        report_type, session_id = "TestReport", "Test QA Test"
        report_item = ReportItem(report_type, session_id)

        _response = api_client.reporting_svc.add_bulk_analytics_report(self.client_, [self.report_item, report_item])

        assert _response[1].status_code == 201
        assert _response[1].reason == 'Created'

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_add_bulk_analytics_report_negative(self):
        allure.step("Verify that without authorization status code is 401")
        report_type, session_id = "TestReport", "Test QA Test"
        report_item = ReportItem(report_type, session_id)

        api_ = ApiClient()
        _response = api_.reporting_svc.add_bulk_analytics_report(self.client_, [self.report_item, report_item])

        assert isinstance(_response[0], dict)
        assert "timestamp" and "status" and "error" and "message" and "path" in _response[0].keys()
        assert _response[0]['error'] == "Unauthorized"
        assert _response[0]['message'] == "the token received is not valid: No token was provided"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
