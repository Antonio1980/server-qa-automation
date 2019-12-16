import allure
import pytest
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.instruments.api_client import ApiClient
from src.base.entities.bounding_box import BoundingBox
from src.base.utils.log_decorator import automation_logger
from src.base.utils.utils import Utils

test_case = "ADD AREAS"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service responded on 'AddAreas' request properly.
    2. Check that service response contains desired properties.
    3. Negative: Check that without authorization it forbidden.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/areas_blacklist_service_tests/add_areas_test.py",
                 "TestAddAreas")
@pytest.mark.regression
@pytest.mark.regression_areas_blacklist
class TestAddAreas:

    ne_lat, ne_lng = 32.09434632337351, 34.82932599989067
    sw_lat, sw_lng = 32.039067310341956, 34.75310834852348
    tel_aviv_box = BoundingBox().set_bounding_box(ne_lat, ne_lng, sw_lat, sw_lng)

    @automation_logger(logger)
    def test_add_areas_method_works(self, api_client):
        allure.step("Verify that response is not empty and status code is 201")
        # sw_lng, sw_lat, ne_lng, ne_lat
        _response = api_client.areas_blacklist_svc.add_areas(Utils.get_random_string(), self.tel_aviv_box)

        assert _response[0] is not None
        assert _response[1].status_code == 201
        assert _response[1].reason == "Created"

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_add_areas_method(self, api_client):
        allure.step("Verify response properties and that service response has 'areas' is list and it > 0")
        _response = api_client.areas_blacklist_svc.add_areas(Utils.get_random_string(), self.tel_aviv_box)[0]

        assert isinstance(_response, dict)
        assert "hash" in _response.keys() and isinstance(_response["hash"], str)
        assert "areas" in _response.keys() and isinstance(_response["areas"], list)
        assert len(_response["areas"]) > 0
        for item in _response["areas"]:
            assert isinstance(item, dict)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_add_areas_negative(self):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        _response = api_.areas_blacklist_svc.add_areas(Utils.get_random_string(), self.tel_aviv_box)

        assert isinstance(_response[0], dict)
        assert "name" and "message" and "code" and "status" and "inner" in _response[0].keys()
        assert _response[0]['code'] == "credentials_required"
        assert _response[0]['message'] == "No authorization token was found"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
