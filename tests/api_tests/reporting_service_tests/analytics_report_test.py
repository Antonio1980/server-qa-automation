import os
import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.entities.report_item import ReportItem
from src.common.log_decorator import automation_logger

test_case = ""


@pytest.mark.skipif(os.environ.get("ENV") == "prod", reason="This test shouldn't run on production!")
@allure.title("ANALYTICS REPORT")
@allure.description("""
    Functional test.
    1. Check that "analytics" request returned status 201- Created.
    """)
@pytest.mark.usefixtures("run_time_count")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/api_tests/reporting_service_tests/analytics_report_test.py",
                 "TestAnalyticsReport")
@pytest.mark.regression
@pytest.mark.reporting_service
class TestAnalyticsReport(object):

    @automation_logger(logger)
    @allure.step("Verify that service returns valid status code and reason.")
    def test_analytics_report(self):
        client_id = "QA"
        report_type, session_id = "TestReport", "Test QA Test"
        report_item = ReportItem(report_type, session_id)

        _response = ApiClient().reporting_svc.analytics_report(client_id, report_item)

        assert _response[1].status_code == 201
        assert _response[1].reason == 'Created'

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")