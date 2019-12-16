import allure
import pytest
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.data_bases.mongo_cli import MongoCli
from src.base.utils.log_decorator import automation_logger

test_case = "TASK SAVED IN MONGO"


@allure.title(test_case)
@allure.description("""
    Functional tests.
    1. Verify that uploaded Task is saved in Mongo DB.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "functional_tests/task_saved_in_mongo_test.py", "TestTaskSavedInMongo")
@pytest.mark.usefixtures("get_uploaded_task", "env")
@pytest.mark.functional
class TestTaskSavedInMongo(object):
    collection_name = "tasks"

    @automation_logger(logger)
    def test_task_saved_in_mongo(self, env, get_uploaded_task):
        allure.step("Verify that uploaded task is saved in Mongo with status 'Done'")

        task_id = get_uploaded_task['taskid']
        db_name = "log-fetch-service-" + env
        query = {"taskid": task_id}
        q_result = MongoCli().find_by_query(db_name, self.collection_name, query)

        get_uploaded_task.update({"status": "Done"})
        q_result.update({"_id": q_result['_id']["$oid"]})
        q_result.pop("__v")

        assert isinstance(q_result, dict)
        assert get_uploaded_task == q_result

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
