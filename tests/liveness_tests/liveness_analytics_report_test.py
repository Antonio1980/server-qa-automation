import allure
import pytest
from src.common import logger
from src.common.utils.slack import Slack
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.entities.report_item import ReportItem
from src.common.log_decorator import automation_logger

test_case = "analytics_liveness"


@allure.feature('Liveness')
@allure.story('Client able send analytics report.')
@allure.title("Reporting Service")
@allure.description("""
    Functional test.
    1. Check that "analytics" request returned status 201- Created.
    """)
@pytest.mark.usefixtures("run_time_count")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/liveness_tests/liveness_analytics_report_test.py",
                 "TestLivenessAnalytics")
@pytest.mark.liveness
class TestLivenessAnalyticsReport(object):

    @automation_logger(logger)
    @allure.step("Verify that service returns valid status code and reason.")
    def test_liveness_analytics_report(self):
        client_id = "QA"
        report_type, session_id = "TestReport", "Test QA Test"
        report_item = ReportItem(report_type, session_id)

        _response = ApiClient().reporting_svc.analytics_report(client_id, report_item)

        if _response[1].status_code != 201 or _response[1].reason != 'Created':
            Slack.send_message(
                F"{self.__class__.__name__} test_liveness_analytics_report failed with response: {_response}")

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
