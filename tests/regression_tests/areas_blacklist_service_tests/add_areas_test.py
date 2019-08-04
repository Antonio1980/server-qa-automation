import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.instruments import Instruments
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("ADD AREAS")
@allure.description("""
    Functional tests.
    1. Check that service responded on 'AddAreas' request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/areas_blacklist_service_tests/add_areas_test.py",
                 "TestAddAreas")
@pytest.mark.usefixtures("run_time_count")
@pytest.mark.regression
@pytest.mark.regression_areas_blacklist
class TestAddAreas(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 201")
    def test_add_areas_method_works(self):
        # sw_lng, sw_lat, ne_lng, ne_lat
        response_ = ApiClient().areas_blacklist_svc.add_areas(Instruments.get_random_string(),
                                                              34.820289208679924, 32.009745169079615,
                                                              34.960364892273674, 32.14007552880953)
        assert response_[0] is not None
        assert response_[1].status_code == 201

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties and that service response has 'areas' is list and it > 0")
    def test_attributes_in_add_areas_method(self):
        response_ = ApiClient().areas_blacklist_svc.add_areas(Instruments.get_random_string(),
                                                              34.820289208679924, 32.009745169079615,
                                                              34.960364892273674, 32.14007552880953)[0]
        assert "hash" in response_.keys() and isinstance(response_["hash"], str)
        assert "areas" in response_.keys() and isinstance(response_["areas"], list)
        assert len(response_["areas"]) > 0
        for item in response_["areas"]:
            assert isinstance(item, dict)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
