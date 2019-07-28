import allure
import pytest
from src.common import logger
from src.common.entities.bounding_box import BoundingBox
from src.common.utils.slack import Slack
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.entities.report_item import ReportItem
from src.common.log_decorator import automation_logger
from src.common.automation_error import AutomationError

test_case = "smoke_liveness"


@allure.feature('Liveness')
@allure.story('R&D team wants to know the basic statement of the services.')
@allure.title("Liveness Smoke Tests")
@allure.description("""
    Functional test.
    1. AreasBlacklist svc: Check that "get_areas_inbox" request returned not empty "areas" list.
    2. Reporting svc: Check that "analytics" request returned status 201- Created.
    3. RemoteConfig svc: Check that "get_config" request returned current config.
    4. Messages svc: Check that "get_user_messages" request returned messages of provided user_id.
    """)
@pytest.mark.usefixtures("run_time_count")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/liveness_tests/liveness_smoke_test.py",
                 "TestSmokeLiveness")
@pytest.mark.liveness
class TestSmokeLiveness(object):
    issues = None

    @automation_logger(logger)
    @allure.step("Verify that service returns areas of TelAviv.")
    def test_get_area_tel_aviv(self):
        ne_lat, ne_lng = 32.09434632337351, 34.82932599989067
        sw_lat, sw_lng = 32.039067310341956, 34.75310834852348
        box = BoundingBox().set_bounding_box(ne_lat, ne_lng, sw_lat, sw_lng)

        _response = ApiClient().areas_blacklist_svc.get_areas_inbox(box)
        if _response[1].status_code != 200 or _response[0] is None or "areas" not in _response[0].keys() \
                or len(_response[0]["areas"]) <= 0:
            TestSmokeLiveness.issues += F"{self.__class__.__name__} test_get_area_tel_aviv failed with response: " \
                F"{_response} \n"

            raise AutomationError(F"Test case {test_case} /1 failed!")

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify that service returns valid status code and reason.")
    def test_liveness_analytics_report(self):
        client_id = "QA"
        report_type, session_id = "TestReport", "Test QA Test"
        report_item = ReportItem(report_type, session_id)

        _response = ApiClient().reporting_svc.analytics_report(client_id, report_item)

        if _response[1].status_code != 201 or _response[1].reason != 'Created':
            TestSmokeLiveness.issues += F"{self.__class__.__name__} test_liveness_analytics_report failed with " \
                F"response: {_response} \n"

            raise AutomationError(F"Test case {test_case} /2 failed!")

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify that service returns remote config data.")
    def test_get_remote_config_liveness(self):
        _response = ApiClient().remote_config_svc.get_config()

        if _response[1].status_code != 200 or _response[0] is None \
                or "_id" and "hash" and "data" not in _response[0].keys() or not isinstance(_response[0]["data"], dict):
            TestSmokeLiveness.issues += F"{self.__class__.__name__} test_get_remote_config_liveness failed with " \
                F"response: {_response} \n"

            raise AutomationError(F"Test case {test_case} /3 failed!")

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")

    @automation_logger(logger)
    @allure.step("Verify that service returns messges per user id")
    def test_user_messages_liveness(self):
        _response = ApiClient().messages_svc.get_user_messages("aaa")

        if _response[1].status_code != 200 or _response[0] is None or "messages" not in _response[0].keys() \
                or not isinstance(_response[0]["messages"], list) or len(_response[0]["messages"]) <= 0:
            TestSmokeLiveness.issues += F"{self.__class__.__name__} test_user_messages_liveness failed with response: "\
                F"{_response} \n"

        if TestSmokeLiveness.issues:
            logger.logger.error(F"Next errors will be sent to Slack (:  {TestSmokeLiveness.issues}")
            Slack.send_message(TestSmokeLiveness.issues)
            raise AutomationError(F"Test case {test_case} /4 failed!")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} PASSED  (all ports), nothing was send. ===========")
