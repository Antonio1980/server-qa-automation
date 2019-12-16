import time
import allure
import pytest

from src.common.enums.enums import DetectedType
from src.common.utils import logger
from config_definitions import BaseConfig
from src.common.instruments.api_client import ApiClient
from src.common.entities.route import Route
from src.common.utils.log_decorator import automation_logger

test_case = "ROUTING CACHE"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Verify that sending 'KeepAlive' request for 5 sec. will create Route record in Routing svc cache.
    2. Verify that if 'KeepAlive' didn't send for 4 sec. Route record will be removed from Routing svc. cache.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "functional_tests/routing_service_cache_test.py", "TestRoutingSvcCache")
@pytest.mark.usefixtures("endpoints")
@pytest.mark.functional
class TestRoutingSvcCache(object):

    route = Route().set_route(ip=Route().ip, name="AntonQA", priority=1, port_list=[88, 99])

    api_ = ApiClient()
    _endpoints = None

    @automation_logger(logger)
    def test_routing_svc_cache(self, endpoints):
        allure.step("Verify that new Route can be saved in Routing service cache.")
        cars = 500
        pedestrian = 1000
        bikes = 100

        run_time = time.perf_counter() + 5.0
        while time.perf_counter() <= run_time:
            time.sleep(0.8)
            self.api_.routing_svc.keep_alive(self.route, cars, pedestrian, bikes)

        allure.step("Verify that My Endpoint is returned from Service cache.")
        TestRoutingSvcCache._endpoints = self.api_.routing_svc.get_endpoints()[0]

        assert isinstance(TestRoutingSvcCache._endpoints, list)
        assert len(TestRoutingSvcCache._endpoints) > 0 and len(TestRoutingSvcCache._endpoints) == len(endpoints) + 1
        for item in TestRoutingSvcCache._endpoints:
            assert isinstance(item, dict)

        my_endpoint = TestRoutingSvcCache._endpoints[-1]
        assert "primaryBoundary" and "insideBoundary" and "outsideBoundary" and "distantBoundary" in my_endpoint.keys()
        assert my_endpoint["ip"] == self.route.ip
        assert my_endpoint["name"] == self.route.name
        assert my_endpoint["priority"] == self.route.priority
        assert my_endpoint["minPort"] == self.route.min_port and my_endpoint["maxPort"] == self.route.max_port
        assert my_endpoint["countByType"][DetectedType.BIKE.value] == bikes and \
               my_endpoint["countByType"][DetectedType.CAR.value] == cars and \
               my_endpoint["countByType"][DetectedType.PEDESTRIAN.value] == pedestrian

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_endpoints_after(self, endpoints):
        time.sleep(4.0)
        allure.step("Verify that My Endpoint is removed from svc. cache if keep alive request didn't send for 4 sec.")
        endpoints_after = self.api_.routing_svc.get_endpoints()[0]

        assert len(endpoints) == len(endpoints_after)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
