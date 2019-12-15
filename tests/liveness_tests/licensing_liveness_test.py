import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger

test_case = "LICENSING LIVENESS"


@allure.feature("LIVENESS")
@allure.story("")
@allure.title(test_case)
@allure.description("""
    
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "liveness_tests/licensing_liveness_test.py", "TestLicensingLiveness")
@pytest.mark.liveness
class TestLicensingLiveness(object):

    @automation_logger(logger)
    def test_get_full_config(self, api_client):
        allure.step("Verify that status code is 200 and response properties."
                    "Verify response properties and that response is dict.")
        _response = api_client.licensing_svc.get_full_config()

        assert _response[0] is not None
        assert _response[1].status_code == 200
        assert _response[1].reason == "OK"
        assert isinstance(_response[0], dict)
        assert "clients" in _response[0].keys()
        assert isinstance(_response[0]["clients"], list)
        assert len(_response[0]["clients"]) > 0
        assert "name" and "_id" and "apiKeys" in _response[0]["clients"][0].keys()
        assert isinstance(_response[0]["clients"][0]["apiKeys"], list)
        assert len(_response[0]["clients"][0]["apiKeys"]) > 0
        assert "applicationIds" and "_id" and "key" and "quotaWarning" and "quotaError" in \
               _response[0]["clients"][0]["apiKeys"][0].keys()

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_validate_client(self, api_client):
        allure.step("Verify that status code is 200 and response properties."
                    "Verify response properties and that response is dict.")
        _response = api_client.licensing_svc.validate_client("C", "api_id", "client_id")

        assert _response[0] is not None
        assert _response[1].status_code == 200
        assert _response[1].reason == "OK"
        assert isinstance(_response[0], dict)
        assert "responseType" in _response[0].keys()
        assert _response[0]["responseType"] == "OK"

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

