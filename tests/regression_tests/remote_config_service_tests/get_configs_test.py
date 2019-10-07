import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = "GET REMOTE CONFIGS"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "GetRemoteConfigs" request properly.
    2. Check that service response contains desired properties.
    3. Check that service returned 404 on not existing config name.
    """)
@pytest.mark.usefixtures("run_time_counter", )
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/remote_config_service_tests/get_configs_test.py",
                 "TestGetRemoteConfigs")
@pytest.mark.regression
@pytest.mark.regression_remote_config
class TestGetRemoteConfigs(object):

    @automation_logger(logger)
    def test_get_remote_configs_method_works(self):
        allure.step("Verify that response is not empty and status code is 200")
        _response = ApiClient().remote_config_svc.get_configs()

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_get_remote_configs(self):
        allure.step("Verify response properties and that 'data' is dict object.")
        _response = ApiClient().remote_config_svc.get_configs()[0]

        assert isinstance(_response, list)
        assert "_id" and "hash" and "data" and "last_updated" and "name" and "description" in _response[0].keys()
        assert _response[0]["name"] == "default"
        assert _response[0]["description"] == "default config"
        assert isinstance(_response[0]["data"], dict)
        assert "swagger" and "param1" and "param2" and "param3" in _response[0]["data"].keys()

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_get_remote_configs_negative(self):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        api_.routing_svc.headers.pop("Authorization")
        _response = api_.remote_config_svc.get_configs()

        assert isinstance(_response[0], dict)
        assert "name" and "message" and "code" and "status" and "inner" in _response[0].keys()
        assert _response[0]['code'] == "credentials_required"
        assert _response[0]['message'] == "No authorization token was found"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
