import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger
from src.common.utils.utils import Utils

test_case = "ADD CLIENT"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Check that service responded on 'AddClient' request properly.
    2. Check that service response contains desired properties.
    3. Negative: Check that without authorization it forbidden.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/licensing_service_tests/add_api_client_test.py",
                 "TestAddApiClient")
@pytest.mark.regression
@pytest.mark.regression_licensing
class TestAddClient:

    name1 = Utils.get_random_string(size=6)
    name2 = Utils.get_random_string(size=6)

    @automation_logger(logger)
    def test_add_client_method_works(self, api_client, api_key):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.licensing_svc.add_client(self.name1, api_key.__dict__)

        assert _response[0] is not None
        assert _response[1].status_code == 200
        assert _response[1].reason == "OK"

        api_client.licensing_svc.delete_client(self.name1)

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_add_client_method(self, api_client, api_key):
        allure.step("Verify response properties and that i")
        _response = api_client.licensing_svc.add_client(self.name2, api_key.__dict__)[0]

        assert isinstance(_response, dict)
        assert "clients" in _response.keys()
        assert isinstance(_response["clients"], dict)
        assert "name" and "apiKeys" in _response["clients"].keys()
        assert isinstance(_response["clients"]["apiKeys"], list)
        assert len(_response["clients"]["apiKeys"]) > 0
        assert "applicationIds" and "_id" and "key" and "quotaWarning" and "quotaError" in _response["clients"]["apiKeys"][0].keys()

        api_client.licensing_svc.delete_client(self.name2)

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_add_client_negative(self, api_key):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        _response = api_.licensing_svc.add_client("abc", api_key.__dict__)

        assert isinstance(_response[0], dict)
        assert "name" and "message" and "code" and "status" and "inner" in _response[0].keys()
        assert _response[0]['code'] == "credentials_required"
        assert _response[0]['message'] == "No authorization token was found"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
