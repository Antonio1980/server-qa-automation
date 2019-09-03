import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.entities.report_item import ReportItem
from src.common.log_decorator import automation_logger

test_case = "ADD ANALYTICS REPORT"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "postReport" request properly.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/routing_service_tests/add_analytics_report_test.py",
                 "TestAddAnalyticsReport")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_routing
class TestAddAnalyticsReport(object):

    report_item = ReportItem("some_type", "some_session_id")

    @automation_logger(logger)
    def test_add_analytics_report_method_works(self):
        allure.step("Verify that response is not empty and status code is 200")
        _response = ApiClient().routing_svc.add_analytics_report("client_", self.report_item)

        assert _response[0] is not None
        assert _response[1].status_code == 201
        assert _response[1].reason == 'Created'

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")
