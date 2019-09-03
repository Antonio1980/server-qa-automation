import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = "GET VERSION INFO"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetVersionInfo" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/reporting_service_tests/get_version_info_test.py",
                 "TestGetVersionInfoReportingSvc")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_reporting
class TestGetVersionInfoReportingSvc(object):

    @automation_logger(logger)
    def test_get_version_info_method_works(self):
        allure.step("Verify that response is not empty and status code is 200")
        _response = ApiClient().reporting_svc.get_version_info()

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_version_info_method(self):
        allure.step("Verify response properties and 'revision' object.")
        _response = ApiClient().reporting_svc.get_version_info()[0]

        assert isinstance(_response, dict)
        assert "appName" and "appVersion" and "buildTime" and "revision" in _response.keys()
        assert _response["appName"] == "reporting-service"
        assert _response["revision"] is not None

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
