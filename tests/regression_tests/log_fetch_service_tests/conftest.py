import pytest
from src.common import logger
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger


@pytest.fixture(scope="class")
@automation_logger(logger)
def task():
    response_ = ApiClient().log_fetch_svc.get_tasks()[0]
    for item in response_["tasks"]:
        if item["userid"] == "any_string" or item["userid"] == "another_any_string" and item["status"] == "Pending":
            return item
    else:
        ApiClient().log_fetch_svc.add_task("any_string")
        task()
