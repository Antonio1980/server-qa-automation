import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = "DELETE REMOTE CONFIG"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "DeleteRemoteConfig" request properly.
    2. Check that service response contains desired properties.
    """)
@pytest.mark.usefixtures("run_time_counter", "add_new_config")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/remote_config_service_tests/delete_config_test.py",
                 "TestDeleteRemoteConfig")
@pytest.mark.regression
@pytest.mark.regression_remote_config
class TestDeleteRemoteConfig(object):

    @automation_logger(logger)
    def test_delete_remote_config(self, add_new_config):
        allure.step("Verify that response is not empty and status code is 200")
        _response = ApiClient().remote_config_svc.delete_remote_config()

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_delete_remote_config_negative(self):
        allure.step("Verify response properties and that 'data' is dict object.")
        _response = ApiClient().remote_config_svc.delete_remote_config()



        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
