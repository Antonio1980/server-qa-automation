import time
import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.entities.bounding_box import BoundingBox
from src.common.entities.route import Route
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("")
@allure.description("""
    Functional tests.
    1. 
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/functional_tests/routing_service_cache_test.py",
                 "TestRoutingSvcCache")
@pytest.mark.usefixtures("run_time_counter", )
@pytest.mark.regression
@pytest.mark.regression_log_fetch
class TestRoutingSvcCache(object):
    box = BoundingBox().set_bounding_box(ne_lat=32.19428911708705, ne_lon=34.769648982994454,
                                         sw_lat=32.166102800738855, sw_lon=34.74080987166633)
    route = Route()
    route = route.set_route(ip=route.ip, name="AntonQA", priority=1, port_list=[88, 99] )

    @automation_logger(logger)
    @allure.step("Verify that ")
    def test_routing_svc_cache(self):
        cars = 500
        pedestrian = 1000
        bikes = 100
        api_ = ApiClient()

        run_time = time.perf_counter() + 5.0
        while time.perf_counter() <= run_time:
            api_.routing_svc.keep_alive(self.box, self.route, cars, pedestrian, bikes)
        time.sleep(3.0)

        endpoints = api_.routing_svc.get_endpoints()[0]
        time.sleep(1.0)
        endpoints_after = api_.routing_svc.get_endpoints()[0]
        # Verify that My Endpoint is returned from Service cache.
        assert isinstance(endpoints, list)
        assert len(endpoints) > 0 and len(endpoints) == 3
        for item in endpoints:
            assert isinstance(item, dict)

        my_endpoint = endpoints[-1]
        assert "primaryBoundary" and "insideBoundary" and "outsideBoundary" and "distantBoundary" in my_endpoint.keys()
        assert my_endpoint["ip"] == self.route.ip
        assert my_endpoint["name"] == self.route.name
        assert my_endpoint["priority"] == self.route.priority
        assert my_endpoint["minPort"] == self.route.min_port and my_endpoint["maxPort"] == self.route.max_port
        assert my_endpoint["countByType"]["BIKE"] == bikes and my_endpoint["countByType"]["CAR"] == cars and \
               my_endpoint["countByType"]["PEDESTRIAN"] == pedestrian

        # Verify that My Endpoint is removed from Service cache.
        assert len(endpoints) - 1 == len(endpoints_after)

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")