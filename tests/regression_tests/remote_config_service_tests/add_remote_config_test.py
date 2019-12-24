import allure
import pytest
from src.base.utils import logger
from src.base.instruments.api_client import ApiClient
from config_definitions import BaseConfig
from src.base.entities.remote_config import RemoteConfig
from src.base.utils.log_decorator import automation_logger
from src.base.utils.utils import Utils

test_case = "ADD REMOTE CONFIG"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "AddRemoteConfig" request properly.
    2. Check that service response contains desired properties.
    3. Negative: Check that without authorization it forbidden.
    4. Negative: Check that with not valid json body it's returned Bad Request..
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/remote_config_service_tests/add_remote_config_test.py",
                 "TestAddRemoteConfig")
@pytest.mark.regression
@pytest.mark.regression_remote_config
class TestAddRemoteConfig:

    @automation_logger(logger)
    def test_add_remote_config_method_works(self, remote_config, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.remote_config_svc.add_remote_config(remote_config)

        assert _response[1].status_code == 200
        assert _response[0] is not None

        del_res = api_client.remote_config_svc.delete_remote_config(remote_config.name)
        assert del_res[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_add_remote_config_method(self, remote_config, api_client):
        allure.step("Verify response properties and that 'data' is dict object.")
        _response = api_client.remote_config_svc.add_remote_config(remote_config)[0]

        assert isinstance(_response, dict)
        assert "_id" and "name" and "hash" and "data" and "description" in _response.keys()
        assert isinstance(_response["data"], dict)
        assert "param1" and "param2" and "param3" and "swagger" in _response["data"].keys()
        assert _response["name"] == remote_config.name

        del_res = api_client.remote_config_svc.delete_remote_config(remote_config.name)
        assert del_res[1].status_code == 200

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_add_remote_config_negative(self):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        remote_config = RemoteConfig(Utils.get_timestamp()).set_config(False, True, 12345, "server-qa-automation")
        _response = api_.remote_config_svc.add_remote_config(remote_config)

        assert isinstance(_response[0], dict)
        assert "name" and "message" and "code" and "status" and "inner" in _response[0].keys()
        assert _response[0]['code'] == "credentials_required"
        assert _response[0]['message'] == "No authorization token was found"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")

    @automation_logger(logger)
    def test_add_remote_config_bad_json(self, api_client):
        allure.step("Verify that broken json causes 400 (Bad Request) error.")

        remote_config = """
        {
            "data": {
                "param1": true, 
                "param2": 12345, 
                "param3": "testing is fun", 
                "swagger": false,
                }, 
            "description": "QA Test", 
            "hash": "1576755879870034", 
            "name": "server-qa-automation"
        }"""

        _response = api_client.remote_config_svc.add_remote_config_negative(remote_config)

        assert _response[1].status_code == 400, "Known Issue # BUG V2X-1882"
        assert isinstance(_response[0], dict)
        assert "err" and "body" and "description" in _response[0].keys()
        assert isinstance(_response[0]["err"], str)
        assert isinstance(_response[0]["body"], str)
        assert isinstance(_response[0]["decription"], str)

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
