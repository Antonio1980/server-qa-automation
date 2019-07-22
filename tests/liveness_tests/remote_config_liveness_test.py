import allure
import pytest
from src.common import logger
from src.common.utils.slack import Slack
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = "remote_config_liveness"


@allure.feature('Liveness')
@allure.story('Client able to get and see remote config (without authorization).')
@allure.title("RemoteConfig Service")
@allure.description("""
    Functional test.
    1. Check that "get_config" request returned current config.
    """)
@pytest.mark.usefixtures("run_time_count")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/liveness_tests/remote_config_liveness_test.py",
                 "TestRemoteConfigLiveness")
@pytest.mark.liveness
class TestRemoteConfigLiveness(object):

    @automation_logger(logger)
    @allure.step("Verify that service returns remote config data.")
    def test_get_remote_config_liveness(self):
        _response = ApiClient().remote_config_svc.get_config()

        if _response[1].status_code != 200 or _response[0] is None \
                or "_id" and "hash" and "data" not in _response[0].keys() or not isinstance(_response[0]["data"], dict):
            Slack.send_message(
                F"{self.__class__.__name__} test_get_remote_config_liveness failed with response: {_response}")

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
