import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.entities.remote_config import RemoteConfig
from src.common.log_decorator import automation_logger
from src.common.utils.utils import Utils

test_case = "DELETE REMOTE CONFIG"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "DeleteRemoteConfig" request properly.
    2. Check that service response contains desired properties.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/remote_config_service_tests/delete_config_test.py",
                 "TestDeleteRemoteConfig")
@pytest.mark.regression
@pytest.mark.regression_remote_config
class TestDeleteRemoteConfig:

    @automation_logger(logger)
    def test_delete_remote_config(self, new_remote_config, api_client):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.remote_config_svc.delete_remote_config(new_remote_config)

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_delete_remote_config_negative(self):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        new_remote_config = RemoteConfig(Utils.get_timestamp()).set_config(False, True, 12345, Utils.get_random_string(6))
        _response = api_.remote_config_svc.delete_remote_config(new_remote_config.name)

        assert isinstance(_response[0], dict)
        assert "name" and "message" and "code" and "status" and "inner" in _response[0].keys()
        assert _response[0]['code'] == "credentials_required"
        assert _response[0]['message'] == "No authorization token was found"
        assert _response[1].status_code == 401

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
