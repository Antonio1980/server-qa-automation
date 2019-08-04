import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.entities.report_item import ReportItem
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("ADD BULK ANALYTICS REPORT")
@allure.description("""
    Functional test.
    1. Check that service is responded on "postReport" request properly.
    """)
@pytest.mark.usefixtures("run_time_count")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/reporting_service_tests/add_bulk_analytics_report_test.py",
                 "TestAddBulkAnalyticsReport")
@pytest.mark.regression
@pytest.mark.regression_reporting
class TestAddBulkAnalyticsReport(object):
    client_id = "TEST"
    report_type, session_id = "QaReport", "Test Report"
    report_item = ReportItem(report_type, session_id)

    @automation_logger(logger)
    @allure.step("Verify that status code is 201")
    def test_add_bulk_analytics_report_method_works(self):
        report_type, session_id = "TestReport", "Test QA Test"
        report_item = ReportItem(report_type, session_id)

        _response = ApiClient().reporting_svc.add_bulk_analytics_report(self.client_id, [self.report_item, report_item])

        assert _response[1].status_code == 201
        assert _response[1].reason == 'Created'

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
