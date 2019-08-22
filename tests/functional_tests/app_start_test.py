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


@allure.title("APP START")
@allure.description("""
    Functional tests.
    1. Check that client app on start sending report "AppStart" and this is saved in Mongo DB.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/functional_tests/app_start_test.py", "TestAppStart")
@pytest.mark.usefixtures("run_time_counter", "env")
@pytest.mark.functional
class TestAppStart(object):
    client_ = AppClient()
    client_id = client_._id
    report_type, session_id = "AppStart", Instruments.get_uuid()
    report_item = ReportItem(report_type, session_id)

    @automation_logger(logger)
    @allure.step("Verify that 'AppStart' report is saved in Mongo -> Reporting svc db -> reportItem ")
    def test_app_start(self, env):
        db_name = "reporting-service-" + env
        collection_name = "reportItem"
        query = {"report.sessionId": self.report_item.session_id}
        _response = ApiClient().reporting_svc.add_analytics_report(self.client_, self.report_item)

        q_result = Instruments.find_by_query(db_name, collection_name, query)

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

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
