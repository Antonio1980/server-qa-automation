import time
import allure
import pytest
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.entities.route import Route
from src.base.enums.enums import DetectedType
from src.base.utils.log_decorator import automation_logger

test_case = "ROUTING CACHE"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Verify that sending 'KeepAlive' request for 5 sec. will create Route record in Routing svc cache.
    2. Verify that if 'KeepAlive' didn't send for 4 sec. Route record will be removed from Routing svc. cache.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "functional_tests/routing_service_cache_test.py", "TestRoutingSvcCache")
@pytest.mark.usefixtures("api_client", "locations")
@pytest.mark.functional
class TestRoutingSvcCache(object):

    route = Route().set_route(ip="127.0.0.1", name="OTHER", priority=1, port_list=[88, 99])

    instances, my_endpoint = None, dict()

    @automation_logger(logger)
    def test_routing_svc_cache(self, api_client, locations):
        allure.step("Verify that new Route can be saved in Routing service cache.")
        cars = 500
        pedestrian = 1000
        bikes = 100
        instance_id = "QA-TEST-QA"

        instances_before = locations["instances"]

        run_time = time.perf_counter() + 5.0
        while time.perf_counter() <= run_time:
            time.sleep(0.8)
            api_client.routing_svc.keep_alive(self.route, instance_id, cars, pedestrian, bikes)

        allure.step("Verify that My Route is returned from Service cache.")
        TestRoutingSvcCache.instances = api_client.routing_svc.get_location_services_v1()[0]["instances"]

        logger.logger.warn(f"++++++++++++{TestRoutingSvcCache.instances}++++++++++++++++")

        assert isinstance(TestRoutingSvcCache.instances, list)
        assert len(TestRoutingSvcCache.instances) > 0 and len(TestRoutingSvcCache.instances) == len(instances_before) + 1
        for item in TestRoutingSvcCache.instances:
            assert isinstance(item, dict)

        for instance_ in TestRoutingSvcCache.instances:
            if instance_["instanceId"] == instance_id:
                self.my_endpoint = instance_

        assert "buildTime" and "revision" and "instanceId" and "definitionId" and "ip" and "minPort" and "maxPort" and\
               "currentLoad" and "region" and "countByType" and "timeStarted" and "provider" and "systemLoad" and \
               "jvmLoad" and "state" and "stateSetAt" in self.my_endpoint.keys()
        assert self.my_endpoint["ip"] == self.route.ip
        assert self.my_endpoint["provider"] == self.route.name
        assert self.my_endpoint["minPort"] == self.route.min_port and self.my_endpoint["maxPort"] == self.route.max_port
        assert self.my_endpoint["countByType"][DetectedType.BIKE.value] == bikes and \
               self.my_endpoint["countByType"][DetectedType.CAR.value] == cars and \
               self.my_endpoint["countByType"][DetectedType.PEDESTRIAN.value] == pedestrian

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_endpoints_after(self, api_client, locations):
        time.sleep(4.0)
        allure.step("Verify that My Endpoint is removed from svc. cache if keep alive request didn't send for 4 sec.")
        endpoints_after = api_client.routing_svc.get_location_services_v1()[0]["instances"]

        assert len(locations["instances"]) == len(endpoints_after)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
