import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.data_bases.mongo_cli import MongoCli
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("TASK SAVED IN MONGO")
@allure.description("""
    Functional tests.
    1. 
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/functional_tests/task_saved_in_mongo_test.py",
                 "TestTaskSavedInMongo")
@pytest.mark.usefixtures("run_time_counter", "get_uploaded_task", "env")
@pytest.mark.regression
@pytest.mark.regression_log_fetch
class TestTaskSavedInMongo(object):
    collection_name = "tasks"

    @automation_logger(logger)
    @allure.step("Verify that uploaded task is saved in Mongo with status 'Done'")
    def test_ask_saved_in_mongo(self, env, get_uploaded_task):
        task_id = get_uploaded_task['taskid']
        db_name = "log-fetch-service-" + env
        query = {"taskid": task_id}
        q_result = MongoCli.find_by_query(db_name, self.collection_name, query)

        get_uploaded_task.update({"status": "Done"})
        q_result.update({"_id": q_result['_id']["$oid"]})
        q_result.pop("__v")

        assert isinstance(q_result, dict)
        assert get_uploaded_task == q_result

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")