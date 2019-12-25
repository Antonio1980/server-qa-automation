import allure
import pytest
from threading import Thread
from src.base.utils import logger
from src.base.instruments.api_client import ApiClient
from src.base.utils.auth_zero import AuthorizationZero
from src.base.utils.log_decorator import automation_logger

test_case = "DELETE USER TASKS"
num_threads = 10
num_loops = 100

_api_client = ApiClient(AuthorizationZero.get_authorization_token()["access_token"])


@pytest.mark.incremental
@pytest.mark.regression
@pytest.mark.regression_log_fetch
@automation_logger(logger)
def test_add_1000_user_messages():
    allure.step("Verify that service able to accept 1000 messages.")

    for _ in range(num_loops):
        _api_client.log_fetch_svc.add_task("server-qa-automation")

    logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")


def test_delete_1000_user_messages():
    allure.step("Verify that service able to delete 1000 messages.")

    _response = _api_client.log_fetch_svc.delete_user_tasks("server-qa-automation")[0]

    assert _response["deletedCount"] == 1100

    logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")


for i in range(num_threads):
    worker = Thread(target=test_add_1000_user_messages)
    worker.setDaemon(True)
    worker.start()
