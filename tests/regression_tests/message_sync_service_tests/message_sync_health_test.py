import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = "HEALTH MESSAGE SYNC"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "Health" request properly.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/message_sync_service_tests/message_sync_health_test.py",
                 "TestHealthMessageSync")
@pytest.mark.regression
@pytest.mark.regression_message_sync
class TestHealthMessageSync:

    @automation_logger(logger)
    def test_health_message_sync(self, api_client):
        allure.step("Verify response status code is 200 and properties of the response.")
        _response = api_client.messages_sync_svc.health()

        assert _response[1].status_code == 200
        assert isinstance(_response[0], dict)
        assert 'memoryUsage' and 'cpuUsage' and 'uptime' and 'version' in _response[0].keys(), "OBJECT KEYS MISMATCHING"
        assert isinstance(_response[0]["memoryUsage"], dict)
        assert "rss" and "heapTotal" and "heapUsed" and "external" in _response[0]["memoryUsage"].keys()
        assert isinstance(_response[0]["cpuUsage"], dict)
        assert "user" and "system" in _response[0]["cpuUsage"]

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
