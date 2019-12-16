import allure
import pytest
from src.common.utils import logger
from config_definitions import BaseConfig
from src.common.utils.log_decorator import automation_logger

test_case = "GET COUNT BY TYPE"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetCountByType" request properly.
    2. Check that service response contains desired properties.
    3. Check that service response on get_count_by_type_v1 (1 version) with empty countByType object. 
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/routing_service_tests/get_count_by_type_test.py",
                 "TestGetCountByType")
@pytest.mark.regression
@pytest.mark.regression_routing
@pytest.mark.client
class TestGetCountByType:

    @automation_logger(logger)
    def test_get_count_by_type_method_works(self, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.routing_svc.get_count_by_type_v2()

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_count_by_type_method(self, api_client):
        allure.step("Verify response properties and that response is list object.")
        _response = api_client.routing_svc.get_count_by_type_v2()[0]

        assert isinstance(_response, dict)
        assert "countByType" in _response.keys()
        assert isinstance(_response["countByType"], dict)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_get_count_by_type_v1_method(self, api_client):
        allure.step("Verify that v1 returned empty.")
        _response = api_client.routing_svc.get_count_by_type_v1()
        assert _response[0] is not None
        assert _response[1].status_code == 200
        assert isinstance(_response[0], dict)
        assert _response[0]["countByType"] is None

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
