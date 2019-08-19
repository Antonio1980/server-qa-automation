import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("EXPORT AREAS")
@allure.description("""
    Functional tests.
    1. Check that service responded on 'ExportAreas' request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/areas_blacklist_service_tests/export_areas_test.py",
                 "TestExportAreas")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_areas_blacklist
class TestExportAreas(object):

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_export_areas_method_works(self):
        _response = ApiClient().areas_blacklist_svc.export_areas()

        assert _response[0] is not None
        assert _response[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify response properties and that service response has 'areas' is list and it > 0")
    def test_attributes_in_export_areas_method(self):
        _response = ApiClient().areas_blacklist_svc.export_areas()[0]

        assert isinstance(_response, dict)
        assert "areas" in _response.keys() and isinstance(_response["areas"], list)
        assert len(_response["areas"]) > 0
        for item in _response["areas"]:
            assert isinstance(item, dict)

        assert "data" in _response.keys() and isinstance(_response["data"], dict)
        assert "areaItems" in _response["data"].keys() and isinstance(_response["data"]["areaItems"], list)
        assert len(_response["data"]["areaItems"]) > 0
        for d in _response["data"]["areaItems"]:
            assert isinstance(d, dict)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
