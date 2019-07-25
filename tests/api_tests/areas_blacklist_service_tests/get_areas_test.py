import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("GET AREAS")
@allure.description("""
    Functional tests.
    1. Check that service responded on 'GetAreas' request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/api_tests/areas_blacklist_service_tests/get_areas_test.py",
                 "TestGetAreas")
@pytest.mark.usefixtures("run_time_count")
@pytest.mark.regression
@pytest.mark.areas_blacklist_service
class TestGetAreas(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_get_areas_method_works(self):
        response_ = ApiClient().areas_blacklist_svc.get_areas()
        assert response_[0] is not None
        assert response_[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify that service response has 'areas' is list and it > 0")
    def test_attributes_in_get_areas_method(self):
        response_ = ApiClient().areas_blacklist_svc.get_areas()[0]
        assert "hash" in response_.keys() and isinstance(response_["hash"], str)
        assert "areas" in response_.keys() and isinstance(response_["areas"], list)
        assert len(response_["areas"]) > 0
        for item in response_["areas"]:
            assert isinstance(item, dict)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
