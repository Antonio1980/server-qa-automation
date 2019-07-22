import allure
import pytest
from src.common import logger
from src.common.utils.slack import Slack
from src.common.api_client import ApiClient
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger

test_case = "area_liveness"


@allure.feature('Liveness')
@allure.story('Client able to get areas of Tel-Aviv using "get_areas_inbox" request properly.')
@allure.title("AreaBlacklist Service")
@allure.description("""
    Functional test.
    1. Check that "get_areas_inbox" request returned not empty "areas" list.
    """)
@pytest.mark.usefixtures("run_time_count")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/liveness_tests/area_liveness_tel_aviv_test.py",
                 "TestAreaLivenessTelAviv")
@pytest.mark.liveness
class TestAreaLivenessTelAviv(object):

    @automation_logger(logger)
    @allure.step("Verify that service returns areas of TelAviv.")
    def test_get_area_tel_aviv(self):
        _response = ApiClient().areas_blacklist_svc.get_areas_inbox(ne_lng=34.82932599989067, ne_lat=32.09434632337351,
                                                                    sw_lng=34.75310834852348, sw_lat=32.039067310341956)
        if _response[1].status_code != 200 or _response[0] is None or "areas" not in _response[0].keys() \
                or len(_response[0]["areas"]) <= 0:
            Slack.send_message(F"{self.__class__.__name__} test_get_area_tel_aviv failed with response: {_response}")

        logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
