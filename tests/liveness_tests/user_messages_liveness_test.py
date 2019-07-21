import allure
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = "messages_liveness"


@allure.feature('Liveness')
@allure.story('Client able to messages per user (without authorization).')
@allure.title("Messages Service")
@allure.description("""
    Functional test.
    1. Check that "get_user_messages" request returned essages of provided user_id.
    """)
@pytest.mark.usefixtures("run_time_count")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/liveness_tests/user_messages_liveness_test.py",
                 "TestUserMesagesLiveness")
@pytest.mark.liveness
class TestUserMesagesLiveness(object):

    @automation_logger(logger)
    @allure.step("Verify that service returns messges per user id")
    def test_user_messages_liveness(self):
        _response = ApiClient().messages_svc.get_user_messages("aaa")

        assert _response[1].status_code == 200
        assert _response[0] is not None
        assert "messages" in _response[0].keys()
        assert isinstance(_response[0]["messages"], list)
        assert len(_response[0]["messages"]) > 0

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
