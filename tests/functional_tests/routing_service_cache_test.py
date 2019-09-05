import time
import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.entities.bounding_box import BoundingBox
from src.common.entities.route import Route
from src.common.log_decorator import automation_logger

test_case = "ROUTING CACHE"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Verify that 'KeepAlive' until 5 sec will create Route in Routing svc cache.
    2. Verify that if 'KeepAlive' didn't send for 4 sec. it will be removed from Routing svc. cache.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/functional_tests/routing_service_cache_test.py",
                 "TestRoutingSvcCache")
@pytest.mark.usefixtures("run_time_counter", )
@pytest.mark.functional
class TestRoutingSvcCache(object):
    box = BoundingBox().set_bounding_box(ne_lat=32.19428911708705, ne_lon=34.769648982994454,
                                         sw_lat=32.166102800738855, sw_lon=34.74080987166633)
    route = Route()
    route = route.set_route(ip=route.ip, name="AntonQA", priority=1, port_list=[88, 99] )

    api_ = ApiClient()
    endpoints = None

    @automation_logger(logger)
    def test_routing_svc_cache(self):
        allure.step("Verify that new Route can be saved in Routing service cache.")
        cars = 500
        pedestrian = 1000
        bikes = 100

        run_time = time.perf_counter() + 5.0
        while time.perf_counter() <= run_time:
            time.sleep(0.8)
            self.api_.routing_svc.keep_alive(self.box, self.route, cars, pedestrian, bikes)

        allure.step("Verify that My Endpoint is returned from Service cache.")
        TestRoutingSvcCache.endpoints = self.api_.routing_svc.get_endpoints()[0]

        assert isinstance(TestRoutingSvcCache.endpoints, list)
        assert len(TestRoutingSvcCache.endpoints) > 0 and len(TestRoutingSvcCache.endpoints) == 3
        for item in TestRoutingSvcCache.endpoints:
            assert isinstance(item, dict)

        my_endpoint = TestRoutingSvcCache.endpoints[-1]
        assert "primaryBoundary" and "insideBoundary" and "outsideBoundary" and "distantBoundary" in my_endpoint.keys()
        assert my_endpoint["ip"] == self.route.ip
        assert my_endpoint["name"] == self.route.name
        assert my_endpoint["priority"] == self.route.priority
        assert my_endpoint["minPort"] == self.route.min_port and my_endpoint["maxPort"] == self.route.max_port
        assert my_endpoint["countByType"]["BIKE"] == bikes and my_endpoint["countByType"]["CAR"] == cars and \
               my_endpoint["countByType"]["PEDESTRIAN"] == pedestrian

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_endpoints_after(self):
        time.sleep(4.0)
        allure.step("Verify that My Endpoint is removed from svc. cache if keep alive request didn't send for 4 sec.")
        endpoints_after = self.api_.routing_svc.get_endpoints()[0]

        assert len(TestRoutingSvcCache.endpoints) - 1 == len(endpoints_after)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
