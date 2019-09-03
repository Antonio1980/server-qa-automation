import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger
from src.common.utils.utils import Utils

test_case = "ADD AREAS"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service responded on 'AddAreas' request properly.
    2. Check that service response contains desired properties.
    3. Negative: Check that without authorization it forbidden.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/areas_blacklist_service_tests/add_areas_test.py",
                 "TestAddAreas")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_areas_blacklist
class TestAddAreas(object):

    @automation_logger(logger)
    def test_add_areas_method_works(self):
        allure.step("Verify that response is not empty and status code is 201")
        # sw_lng, sw_lat, ne_lng, ne_lat
        _response = ApiClient().areas_blacklist_svc.add_areas(Utils.get_random_string(),
                                                              34.820289208679924, 32.009745169079615,
                                                              34.960364892273674, 32.14007552880953)

        assert _response[0] is not None
        assert _response[1].status_code == 201
        assert _response[1].reason == "Created"

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_add_areas_method(self):
        allure.step("Verify response properties and that service response has 'areas' is list and it > 0")
        _response = ApiClient().areas_blacklist_svc.add_areas(Utils.get_random_string(),
                                                              34.820289208679924, 32.009745169079615,
                                                              34.960364892273674, 32.14007552880953)[0]

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
        api_.reporting_svc.headers.pop("Authorization")
        _response = api_.areas_blacklist_svc.add_areas(Utils.get_random_string(),
                                                       34.820289208679924, 32.009745169079615,
                                                       34.960364892273674, 32.14007552880953)

        assert isinstance(_response[0], dict)
        assert "name" and "message" and "code" and "status" and "inner" in _response[0].keys()
        assert _response[0]['code'] == "credentials_required"
        assert _response[0]['message'] == "No authorization token was found"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
