import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.entities.app_client import AppClient
from src.common.entities.report_item import ReportItem
from src.common.log_decorator import automation_logger

test_case = "ADD ANALYTICS REPORT"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "postReport" request properly.
    """)
@pytest.mark.usefixtures("run_time_counter")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/reporting_service_tests/add_analytics_report_test.py",
                 "TestAddAnalyticsReport")
@pytest.mark.regression
@pytest.mark.regression_reporting
class TestAddAnalyticsReport(object):
    client_ = AppClient()
    report_type, session_id = "TestReport", "Test QA Test"
    report_item = ReportItem(report_type, session_id)

    @automation_logger(logger)
    def test_add_analytics_report_method_works(self):
        allure.step("Verify that status code is 201")
        _response = ApiClient().reporting_svc.add_analytics_report(self.client_, self.report_item)

        assert _response[1].status_code == 201
        assert _response[1].reason == 'Created'

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
