import time
import allure
import pytest
from threading import Thread
from src.base.utils import logger
from src.base.instruments.api_client import ApiClient
from src.base.utils.auth_zero import AuthorizationZero
from src.base.utils.log_decorator import automation_logger

test_case = "DELETE USER TASKS"
user_id = "server-qa-automation"
num_threads = 50
num_loops = 20

_api_client = ApiClient(AuthorizationZero.get_authorization_token()["access_token"])
_api_client.log_fetch_svc.delete_user_tasks(user_id)


@pytest.mark.incremental
@pytest.mark.regression
@pytest.mark.regression_log_fetch
@automation_logger(logger)
def test_add_1000_user_messages():
    allure.step(f"Verify that service able to accept {(num_threads * num_loops) + num_loops} messages.")

    for _ in range(num_loops):
        _api_client.log_fetch_svc.add_task(user_id)

    logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")


@pytest.mark.regression
@pytest.mark.regression_log_fetch
@automation_logger(logger)
def test_delete_1000_user_messages():
    allure.step(f"Verify that service able to delete {(num_threads * num_loops) + num_loops} messages.")
    time.sleep(5.0)
    _response = _api_client.log_fetch_svc.delete_user_tasks(user_id)[0]

    assert _response["deletedCount"] == 1020

    logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")


for i in range(num_threads):
    worker = Thread(target=test_add_1000_user_messages)
    worker.setDaemon(True)
    worker.start()
