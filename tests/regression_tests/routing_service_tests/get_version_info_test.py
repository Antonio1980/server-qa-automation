import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("GET VERSION INFO")
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetVersionInfo" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/routing_service_tests/get_version_info_test.py",
                 "TestGetVersionInfo")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_routing
class TestGetVersionInfo(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_get_version_info_method_works(self):
        response_ = ApiClient().routing_svc.get_version_info()

        assert response_[0] is not None
        assert response_[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties and 'revision' object.")
    def test_attributes_in_get_version_info_method(self):
        response_ = ApiClient().routing_svc.get_version_info()[0]

        assert "appName" and "appVersion" and "buildTime" and "revision" in response_.keys()
        assert response_["appName"] == "routing-service"
        assert response_["revision"] is not None

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
