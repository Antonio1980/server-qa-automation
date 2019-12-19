import time
import allure
import pytest
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.entities.location import Location
from src.base.entities.bounding_box import BoundingBox
from src.base.utils.log_decorator import automation_logger

test_case = "ROUTING FUNCTIONAL"


@pytest.mark.incremental
@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Route before.
    2. Update definitions.
    3. Create instance.
    4. Route after. 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "functional_tests/routing_service_test.py", "TestRoutingServiceFunctional")
@pytest.mark.functional
class TestRoutingServiceFunctional(object):
    ne_lat, ne_lng = 68.535766, 139.002884
    sw_lat, sw_lng = 57.309398, 42.634434
    definition_id, nickname = None, None

    russia_box = BoundingBox().set_bounding_box(max_lat=ne_lat, max_lon=ne_lng, min_lat=sw_lat, min_lon=sw_lng)

    location = Location().set_location(60.754702, 70.537105, "RUSSIA")

    @pytest.fixture(scope="class")
    @automation_logger(logger)
    def definition(self, request, api_client):
        _response = api_client.routing_svc.create_location_definitions(self.russia_box, "GOOGLE", 1, "europe-north1-a")
        assert _response[1].status_code == 200

        for item in _response[0]["definitions"]:
            if item["region"] == "europe-north1-a":
                TestRoutingServiceFunctional.definition_id = item["definitionId"]
                res = item

        def clean_definition():
            api_client.routing_svc.delete_location_definitions(TestRoutingServiceFunctional.definition_id)

        request.addfinalizer(clean_definition)

        return res

    @automation_logger(logger)
    def test_route_before(self, api_client):
        allure.step("Verify that ")
        _response = api_client.routing_svc.route_me_v4(self.location)
        assert _response[1].status_code == 200
        assert "default" in _response[0]["name"]

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_create_instance(self, api_client, definition):
        allure.step("Verify that ")
        TestRoutingServiceFunctional.definition_id = definition["definitionId"]
        TestRoutingServiceFunctional.nickname = definition["nickname"]

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_route_after(self, api_client):
        allure.step("Verify that ")
        time.sleep(240.0)
        _response = api_client.routing_svc.route_me_v4(self.location)
        assert _response[1].status_code == 200
        assert TestRoutingServiceFunctional.nickname == _response[0]["name"]

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")