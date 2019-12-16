import allure
import pytest
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.utils.log_decorator import automation_logger

test_case = "LIVENESS HEALTH"


@allure.feature("LIVENESS")
@allure.story("R&D team wants to know the 'Health' status of the services.")
@allure.title(test_case)
@allure.description("""
    Health tests.
    1. Liveness for AreasBlackList service.
    2. Liveness for LogFetch service.
    3. Liveness for MessageSync service.
    4. Liveness for Message service.
    5. Liveness for RemoteConfig service.
    6. Liveness for Reporting service.
    7. Liveness for Routing service.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "liveness_tests/liveness_health_test.py", "TestHealthLiveness")
@pytest.mark.liveness
class TestHealthLiveness(object):

    @automation_logger(logger)
    def test_health_areas_black_list(self, api_client):
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

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_health_log_fetch(self, api_client):
        allure.step("Verify that status code is 200 and response properties.")

        _response = api_client.log_fetch_svc.health()

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

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

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

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")

    @automation_logger(logger)
    def test_health_message(self, api_client):
        allure.step("Verify that status code is 200 and response properties.")

        _response = api_client.message_svc.health()

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

        logger.logger.info(F"============ TEST CASE {test_case} / 4 PASSED ===========")

    @automation_logger(logger)
    def test_health_remote_config(self, api_client):
        allure.step("Verify that status code is 200 and response properties.")

        _response = api_client.remote_config_svc.health()

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
    def test_health_reporting(self, api_client):
        allure.step("Verify response status code is 200 and properties of the response.")

        _response = api_client.reporting_svc.health()

        assert _response[1].status_code == 200
        assert isinstance(_response[0], dict)
        assert "status" in _response[0].keys()
        assert _response[0]["status"] == "UP"

        logger.logger.info(F"============ TEST CASE {test_case} / 6 PASSED ===========")

    @automation_logger(logger)
    def test_health_routing(self, api_client):
        allure.step("Verify response status code is 200 and properties of the response.")

        _response = api_client.routing_svc.health()

        assert _response[1].status_code == 200
        assert isinstance(_response[0], dict)
        assert "status" in _response[0].keys()
        assert _response[0]["status"] == "UP"

        logger.logger.info(F"============ TEST CASE {test_case} / 8 PASSED ===========")
