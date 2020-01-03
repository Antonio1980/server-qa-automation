import allure
import pytest
from src.base.lib_ import logger
from config_definitions import BaseConfig
from src.base.lib_.log_decorator import automation_logger

test_case = "HEALTH AREAS BLACKLIST"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service responded on 'Health' request properly and that "mongooseStatus" is UP.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/areas_blacklist_service_tests/areas_blacklist_health_test.py",
                 "TestHealthAreasBlackList")
@pytest.mark.regression
@pytest.mark.regression_areas_blacklist
class TestHealthAreasBlackList:

    @automation_logger(logger)
    def test_health_area_black_list(self, api_client):
        allure.step("Verify that status code is 200 and response properties.")
        _response = api_client.areas_blacklist_svc.health()

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
