import pytest
from src.common import logger
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger


@pytest.fixture
@automation_logger(logger)
def get_task():
    response_ = ApiClient().log_fetch_svc.get_tasks()[0]

    for item in response_["tasks"]:
        if (item["userid"] == "any_string" or item["userid"] == "another_any_string") and item["status"] == "Pending":
            return item
    else:
        ApiClient().log_fetch_svc.add_task("any_string")
        get_task()


@pytest.fixture
@automation_logger(logger)
def get_uploaded_task(get_task):
    task_id = get_task["taskid"]
    try:
        return ApiClient().log_fetch_svc.upload_file_task(task_id, " Do the current tasks")[0]
    except Exception as e:
        logger.logger(F"Error on fixture get_uploaded_task: {e}")
        raise e
