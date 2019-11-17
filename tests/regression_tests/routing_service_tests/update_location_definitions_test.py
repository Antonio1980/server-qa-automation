import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.entities.bounding_box import BoundingBox
from src.common.log_decorator import automation_logger

test_case = "UPDATE LOCATION DEFINITIONS"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "updateLocationServices" request properly.
    2. Check that service response contains desired properties.
    3. Check that service response on get_count_by_type_v1 (1 version) with empty countByType object. 
    """)
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.usefixtures("run_time_counter", )
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/routing_service_tests/update_location_definitions_test.py",
                 "TestUpdateLocationDefinitions")
@pytest.mark.regression
@pytest.mark.regression_routing
@pytest.mark.client
class TestUpdateLocationDefinitions:

    ne_lat, ne_lng = 32.09434632337351, 34.82932599989067
    sw_lat, sw_lng = 32.039067310341956, 34.75310834852348
    tel_aviv_box = BoundingBox().set_bounding_box(ne_lat, ne_lng, sw_lat, sw_lng)

    @automation_logger(logger)
    def test_update_definitions_method_works(self, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.routing_svc.update_location_definitions(self.tel_aviv_box, "", 1, "")

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_update_definitions_method(self, api_client):
        allure.step("Verify response properties in response object.")
        _response = api_client.routing_svc.update_location_definitions(self.tel_aviv_box, "", 1, "")[0]

        assert "definitions" and "instances" in _response.keys()
        assert isinstance(_response["definitions"], list)
        assert len(_response["definitions"]) > 0
        assert isinstance(_response["instances"], list)
        assert len(_response["instances"]) > 0

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_update_definitions_negative(self):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        _response = api_.routing_svc.update_location_definitions(self.tel_aviv_box, "", 1, "")

        assert isinstance(_response[0], dict)
        assert "timestamp" and "status" and "error" and "message" and "path" in _response[0].keys()
        assert _response[0]['error'] == "Unauthorized"
        assert _response[0]['message'] == "the token received is not valid: No token was provided"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
