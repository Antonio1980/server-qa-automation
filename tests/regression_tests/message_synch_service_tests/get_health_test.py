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
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_messages_synch
class TestGetHealth(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_get_health_method_works(self):
        _response = ApiClient().messages_synch_svc.get_health()
        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties as dictionary keys.")
    def test_attributes_in_get_health_method(self):
        _response = ApiClient().messages_synch_svc.get_health()[0]

        assert isinstance(_response, dict)
        assert 'memoryUsage' and 'cpuUsage' and 'uptime' and 'version' in _response.keys(), "OBJECT KEYS MISMATCHING"
        assert isinstance(_response["memoryUsage"], dict)
        assert "rss" and "heapTotal" and "heapUsed" and "external" in _response["memoryUsage"].keys()
        assert isinstance(_response["cpuUsage"], dict)
        assert "user" and "system" in _response["cpuUsage"]

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
