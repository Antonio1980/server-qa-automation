import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("GET HEALTH")
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetHealth" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/message_synch_service_tests/get_health_test.py",
                 "TestGetHealth")
@pytest.mark.usefixtures("run_time_count")
@pytest.mark.regression
@pytest.mark.regression_messages_synch_service
class TestGetHealth(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_get_health_method_works(self):
        response_ = ApiClient().messages_synch_svc.get_health()
        assert response_[0] is not None
        assert response_[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties as dictionary keys.")
    def test_attributes_in_get_health_method(self):
        response_ = ApiClient().messages_synch_svc.get_health()[0]
        assert "nodeHealth" and "mongooseHealth" and "serviceVersion" in response_.keys()
        assert isinstance(response_["nodeHealth"], dict) and isinstance(response_["mongooseHealth"], dict) and \
               isinstance(response_["serviceVersion"], dict)
        assert 'memoryUsage' and 'cpuUsage' and 'uptime' and 'version' in response_["nodeHealth"].keys()
        assert 'mongooseStatus' in response_["mongooseHealth"].keys()
        assert 'version' in response_["serviceVersion"].keys()

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
