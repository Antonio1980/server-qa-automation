import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("GET COUNT BY TYPE")
@allure.description("""
    Functional tests.
    1. Check that service is responded on "GetCountByType" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/routing_service_tests/get_count_by_type_test.py",
                 "TestGetCountByType")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_routing
class TestGetCountByType(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_get_count_by_type_method_works(self):
        _response = ApiClient().routing_svc.get_count_by_type()

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties and that response is list object.")
    def test_attributes_in_get_count_by_type_method(self):
        _response = ApiClient().routing_svc.get_count_by_type()[0]

        assert isinstance(_response, dict)
        assert "countByType" in _response.keys()
        assert isinstance(_response["countByType"], dict)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
