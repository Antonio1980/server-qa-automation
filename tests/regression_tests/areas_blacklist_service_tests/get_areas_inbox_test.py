import allure
import pytest
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.entities.bounding_box import BoundingBox
from src.base.utils.log_decorator import automation_logger

test_case = "GET AREAS IN BOX"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service responded on 'GetAreasInBox' request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/areas_blacklist_service_tests/get_areas_in_box_test.py",
                 "TestGetAreasInBox")
@pytest.mark.regression
@pytest.mark.regression_areas_blacklist
@pytest.mark.client
class TestGetAreasInBox:

    ne_lat, ne_lng = 32.09434632337351, 34.82932599989067
    sw_lat, sw_lng = 32.039067310341956, 34.75310834852348
    tel_aviv_box = BoundingBox().set_bounding_box(ne_lat, ne_lng, sw_lat, sw_lng)

    @automation_logger(logger)
    def test_get_areas_in_box_method_works(self, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.areas_blacklist_svc.get_areas_inbox(self.tel_aviv_box)

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_areas_in_box_method(self, api_client):
        allure.step("Verify response properties and that service response has 'areas' is list and it > 0")
        _response = api_client.areas_blacklist_svc.get_areas_inbox(self.tel_aviv_box)[0]

        assert isinstance(_response, dict)
        assert "hash" in _response.keys() and isinstance(_response["hash"], str)
        assert "areas" in _response.keys() and isinstance(_response["areas"], list)
        assert len(_response["areas"]) > 0
        for item in _response["areas"]:
            assert isinstance(item, dict)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
