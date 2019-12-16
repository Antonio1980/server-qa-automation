import allure
import pytest
from src.common.utils import logger
from config_definitions import BaseConfig
from src.common.instruments.api_client import ApiClient
from src.common.utils.log_decorator import automation_logger

test_case = "ACTIVATE AREA"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service responded on 'ActivateArea' request properly.
    2. Check that service response contains desired properties.
    3. Negative: Check that without authorization it forbidden.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/areas_blacklist_service_tests/activate_test.py",
                 "TestActivateArea")
@pytest.mark.regression
@pytest.mark.regression_areas_blacklist
class TestActivateArea:

    @automation_logger(logger)
    def test_activate_area_method_works(self, get_area, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.areas_blacklist_svc.activate_area(get_area["_id"], True)

        assert _response[0] is not None
        assert _response[1].status_code == 200
        assert _response[1].reason == "OK"

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_activate_area_method(self, get_area, api_client):
        allure.step("Verify response properties and that isActive is false.")
        _response = api_client.areas_blacklist_svc.activate_area(get_area["_id"], False)[0]

        assert isinstance(_response, dict)
        assert "isActive" and "_id" and "description" and "position" in _response.keys()
        assert _response["isActive"] is False
        assert _response["_id"] == get_area["_id"]
        assert "qa_test_qa" in _response["description"]

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_activate_area_negative(self, get_area):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        _response = api_.areas_blacklist_svc.activate_area(get_area["_id"], True)

        assert isinstance(_response[0], dict)
        assert "name" and "message" and "code" and "status" and "inner" in _response[0].keys()
        assert _response[0]['code'] == "credentials_required"
        assert _response[0]['message'] == "No authorization token was found"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
