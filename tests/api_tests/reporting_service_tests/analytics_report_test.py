import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.entities.report_item import ReportItem
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("ANALYTICS REPORT")
@allure.description("""
    Functional test.
    1. Check that service is responded on "GetRemoteConfig" request properly.
    """)
@pytest.mark.usefixtures("run_time_count")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/api_tests/reporting_service_tests/analytics_report_test.py",
                 "TestAnalyticsReport")
@pytest.mark.regression
@pytest.mark.reporting_service
class TestAnalyticsReport(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 201")
    def test_analytics_report_method_works(self):
        client_id = "QA"
        report_type, session_id = "TestReport", "Test QA Test"
        report_item = ReportItem(report_type, session_id)

        _response = ApiClient().reporting_svc.analytics_report(client_id, report_item)

        assert _response[1].status_code == 201
        assert _response[1].reason == 'Created'

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
