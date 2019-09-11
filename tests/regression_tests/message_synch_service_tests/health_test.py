import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = "HEALTH MESSAGES SYNCH"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "Health" request properly.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/message_synch_service_tests/health_test.py",
                 "TestHealth")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_messages_synch
class TestHealth(object):

    @automation_logger(logger)
    def test_health_message_synch(self):
        allure.step("Verify response status code is 200 and properties of the response.")
        _response = ApiClient().messages_synch_svc.health()

        assert _response[1].status_code == 200
        assert isinstance(_response[0], dict)
        assert 'memoryUsage' and 'cpuUsage' and 'uptime' and 'version' in _response[0].keys(), "OBJECT KEYS MISMATCHING"
        assert isinstance(_response[0]["memoryUsage"], dict)
        assert "rss" and "heapTotal" and "heapUsed" and "external" in _response[0]["memoryUsage"].keys()
        assert isinstance(_response[0]["cpuUsage"], dict)
        assert "user" and "system" in _response[0]["cpuUsage"]

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
