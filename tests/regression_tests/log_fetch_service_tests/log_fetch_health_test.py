import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = "HEALTH LOG FETCH"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service responded on 'Health' request properly and that "mongooseStatus" is UP.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/log_fetch_service_tests/log_fetch_health_test.py",
                 "TestHealthLogFetch")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_log_fetch
class TestHealthLogFetch(object):

    @automation_logger(logger)
    def test_health_log_fetch(self):
        allure.step("Verify that status code is 200 and response properties.")
        _response = ApiClient().log_fetch_svc.health()

        assert _response[1].status_code == 200
        assert isinstance(_response[0], dict)
        assert "nodeHealth" and "mongooseHealth" and "serviceVersion" in _response[0].keys()
        assert isinstance(_response[0]["nodeHealth"], dict)
        assert "memoryUsage" and "cpuUsage" and "uptime" and "version" in _response[0]["nodeHealth"].keys()
        assert isinstance(_response[0]["nodeHealth"]["memoryUsage"], dict)
        assert "rss" and "heapTotal" and "heapUsed" and "external" in _response[0]["nodeHealth"]["memoryUsage"].keys()
        assert isinstance(_response[0]["nodeHealth"]["cpuUsage"], dict)
        assert "user" and "system" in _response[0]["nodeHealth"]["cpuUsage"].keys()
        assert isinstance(_response[0]["mongooseHealth"], dict)
        assert "mongooseStatus" in _response[0]["mongooseHealth"].keys()
        assert _response[0]["mongooseHealth"]["mongooseStatus"] == "UP"
        assert isinstance(_response[0]["serviceVersion"], dict)
        assert "version" in _response[0]["serviceVersion"].keys()

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
