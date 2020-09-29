import allure
import pytest
from src.base.lib_ import logger
from src.base.lib_.log_decorator import automation_logger


test_case = "DELETE USER TASKS"
user_id = "server-qa-automation"
num_threads = 50
num_loops = 20


@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.regression
@pytest.mark.regression_log_fetch
@automation_logger(logger)
class TestDelete1000UserMessages(object):

    @automation_logger(logger)
    def test_delete_1000_user_messages(self, _1000_user_messages, api_client):
        allure.step(f"Verify that service able to delete {(num_threads * num_loops) + num_loops} messages.")

        _response = api_client.log_fetch_svc.delete_user_tasks(user_id)[0]

        assert _response["deletedCount"] == num_threads * num_loops

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
