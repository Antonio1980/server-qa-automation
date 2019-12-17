import allure
import pytest
from src.base.entities.bounding_box import BoundingBox
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.entities.location import Location
from src.base.utils.log_decorator import automation_logger
from src.base.utils.utils import Utils

test_case = "ROUTING FUNCTIONAL"


@pytest.mark.skip
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
@pytest.mark.usefixtures("api_client", "env")
@pytest.mark.functional
class TestRoutingServiceFunctional(object):
    ne_lat, ne_lng = 45.680180, -92.807291
    sw_lat, sw_lng = 37.029238, -113.338244

    def_id = Utils.get_random_string()

    usa_box = BoundingBox().set_bounding_box(max_lat=ne_lat, max_lon=ne_lng, min_lat=sw_lat, min_lon=sw_lng)

    location = Location().set_location(41.542570, -101.662931, "USA")

    @automation_logger(logger)
    def test_route_before(self, api_client):
        allure.step("Verify that ")
        _response = api_client.routing_svc.add_route_v4(self.location)
        assert _response[1].status_code == 200
        assert "default" in _response[0]["name"]

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_create_instance(self, api_client, definition):
        allure.step("Verify that ")
        definition_id = definition["definitionId"]
        _response = api_client.routing_svc.create_location_instance()
        assert _response[1].status_code == 200
        assert "definitions" and "instances" in _response[0].keys()

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")