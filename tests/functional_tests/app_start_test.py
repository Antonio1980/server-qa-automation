import time
import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.instruments import Instruments
from src.common.entities.app_client import AppClient
from src.common.entities.report_item import ReportItem
from src.common.log_decorator import automation_logger

test_case = ""


@pytest.mark.incremental
@allure.title("APP START")
@allure.description("""
    Functional tests.
    1. Check that client app on start sending report "AppStart" and this is saved in Mongo DB.
    2. Check that report saved in Elastic DB as well.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/functional_tests/app_start_test.py", "TestAppStart")
@pytest.mark.usefixtures("run_time_counter", "env")
@pytest.mark.functional
class TestAppStart(object):
    client_ = AppClient()
    client_id = client_._id
    collection_name = "reportItem"
    report_type, session_id = "AppStart", Instruments.get_uuid()
    report_item = ReportItem(report_type, session_id)
    ApiClient().reporting_svc.add_analytics_report(client_, report_item)

    @automation_logger(logger)
    @allure.step("Verify that 'AppStart' report is saved in Mongo -> Reporting svc db -> reportItem")
    def test_report_saved_in_mongo(self, env):
        db_name = "reporting-service-" + env
        query = {"report.sessionId": self.report_item.session_id}
        q_result = Instruments.find_by_query(db_name, self.collection_name, query)

        assert isinstance(q_result, dict)
        assert "_id" and "report" and "source" and "migratedFromMongo" and "env" in q_result.keys()
        assert q_result["_id"] == self.report_item.id
        assert isinstance(q_result["report"], dict)
        assert "sessionId" and "type" and "clientId" and "params" in q_result["report"].keys()
        assert q_result["report"]["sessionId"] == self.report_item.session_id
        assert q_result["report"]["type"] == self.report_item.report_type
        assert q_result["report"]["clientId"] == self.client_._id
        assert isinstance(q_result["report"]["params"], dict)
        assert "generalInfo" in q_result["report"]["params"].keys()
        assert isinstance(q_result["report"]["params"]["generalInfo"], dict)
        assert self.client_.device.__dict__ == q_result["report"]["params"]["generalInfo"]

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify that 'AppStart' report is saved in Elastic -> analytics")
    def test_report_saved_in_elastic(self, env):
        time.sleep(5.0)
        index_ = "analytics-" + env
        query = {"query": {"match": {'report.sessionId': self.report_item.session_id}}}
        q_result = Instruments.search_document(index_, query)

        assert isinstance(q_result, dict)
        assert "took" and "timed_out" and "_shards" and "hits" in q_result.keys()
        assert q_result["timed_out"] is False
        assert isinstance(q_result["hits"], dict)
        assert "total" and "max_score" and "hits" in q_result["hits"].keys()
        assert isinstance(q_result["hits"]["hits"], list)
        assert isinstance(q_result["hits"]["hits"][0], dict)
        assert q_result["hits"]["hits"][0]["_index"] == index_
        assert q_result["hits"]["hits"][0]["_type"] == "_doc"
        assert q_result["hits"]["hits"][0]["_id"] == self.report_item.id
        assert "_source" in q_result["hits"]["hits"][0].keys()
        assert isinstance(q_result["hits"]["hits"][0]["_source"], dict)
        assert q_result["hits"]["hits"][0]["_source"]["id"] == self.report_item.id
        assert "report" in q_result["hits"]["hits"][0]["_source"].keys()
        assert isinstance(q_result["hits"]["hits"][0]["_source"]["report"], dict)
        assert "sessionId" and "type" and "clientId" and "params" in q_result["hits"]["hits"][0]["_source"]["report"].keys()
        assert q_result["hits"]["hits"][0]["_source"]["report"]["sessionId"] == self.report_item.session_id
        assert q_result["hits"]["hits"][0]["_source"]["report"]["type"] == self.report_type
        assert q_result["hits"]["hits"][0]["_source"]["report"]["clientId"] == self.client_id
        assert q_result["hits"]["hits"][0]["_source"]["report"]["params"]["generalInfo"] == self.client_.device.__dict__

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
