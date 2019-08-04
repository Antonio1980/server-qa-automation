import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.entities.report_item import ReportItem
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("ADD ANALYTICS REPORT")
@allure.description("""
    Functional tests.
    1. Check that service is responded on "postReport" request properly.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/routing_service_tests/add_analytics_report_test.py",
                 "TestAddAnalyticsReport")
@pytest.mark.usefixtures("run_time_count")
@pytest.mark.regression
@pytest.mark.regression_routing
class TestAddAnalyticsReport(object):

    report_item = ReportItem("some_type", "some_session_id")

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_add_analytics_report_method_works(self):
        response_ = ApiClient().routing_svc.add_analytics_report("client_", self.report_item)

        assert response_[0] is not None
        assert response_[1].status_code == 201
        assert response_[1].reason == 'Created'

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")
