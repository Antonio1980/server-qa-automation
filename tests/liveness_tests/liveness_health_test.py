import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = "LIVENESS HEALTH"


@allure.feature("LIVENESS")
@allure.story("R&D team wants to know the 'Health' status of the services.")
@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Liveness for AreBlackList service.
    2. Liveness for Location service. - ignored.
    3. Liveness for LogFetch service.
    4. Liveness for MessagesSynch service.
    5. Liveness for Messages service.
    6. Liveness for RemoteConfig service.
    7. Liveness for Reporting service.
    8. Liveness for Routing service.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/liveness_tests/liveness_health_test.py",
                 "TestHealthLiveness")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.liveness
class TestHealthLiveness(object):

    @automation_logger(logger)
    def test_health_area_black_list(self):
        allure.step("Verify that status code is 200 and response properties.")

        _response = ApiClient().areas_blacklist_svc.health()

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

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @pytest.mark.skip
    @automation_logger(logger)
    def test_health_location(self):
        allure.step("Verify response status code is 200 and properties of the response.")

        _response = ApiClient().location_svc.health()

        assert _response[1].status_code == 200
        assert isinstance(_response[0], dict)
        assert "status" in _response[0].keys()
        assert _response[0]["status"] == "UP"

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

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

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")

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

        logger.logger.info(F"============ TEST CASE {test_case} / 4 PASSED ===========")

    @automation_logger(logger)
    def test_health_messages(self):
        allure.step("Verify that status code is 200 and response properties.")

        _response = ApiClient().messages_svc.health()

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

        logger.logger.info(F"============ TEST CASE {test_case} / 5 PASSED ===========")

    @automation_logger(logger)
    def test_health_remote_config(self):
        allure.step("Verify that status code is 200 and response properties.")

        _response = ApiClient().remote_config_svc.health()

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

        logger.logger.info(F"============ TEST CASE {test_case} / 6 PASSED ===========")

    @automation_logger(logger)
    def test_health_reporting(self):
        allure.step("Verify response status code is 200 and properties of the response.")

        _response = ApiClient().reporting_svc.health()

        assert _response[1].status_code == 200
        assert isinstance(_response[0], dict)
        assert "status" in _response[0].keys()
        assert _response[0]["status"] == "UP"

        logger.logger.info(F"============ TEST CASE {test_case} / 7 PASSED ===========")

    @automation_logger(logger)
    def test_health_routing(self):
        allure.step("Verify response status code is 200 and properties of the response.")

        _response = ApiClient().routing_svc.health()

        assert _response[1].status_code == 200
        assert isinstance(_response[0], dict)
        assert "status" in _response[0].keys()
        assert _response[0]["status"] == "UP"

        logger.logger.info(F"============ TEST CASE {test_case} / 8 PASSED ===========")
