import allure
import pytest
from src.common import logger
from config_definitions import BaseConfig
from src.common.api_client import ApiClient
from src.common.entities.bounding_box import BoundingBox
from src.common.entities.route import Route
from src.common.log_decorator import automation_logger

test_case = ""


@allure.title("KEEP ALIVE")
@allure.description("""
    Functional tests.
    1. Check that service is responded on "keepAlive" request properly.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/regression_tests/routing_service_tests/keep_alive_test.py",
                 "TestKeepAlive")
@pytest.mark.usefixtures("run_time_counter")
@pytest.mark.regression
@pytest.mark.regression_routing
class TestKeepAlive(object):

    tel_aviv_box = BoundingBox()

    route = Route().set_route(ip="0.0.0.0", name="QA-Test", priority=1, port_list=[8000, 9000])

    @automation_logger(logger)
    @allure.step("Verify that response is not empty and status code is 200")
    def test_keep_alive_method_works(self):
        response_ = ApiClient().routing_svc.keep_alive(self.tel_aviv_box, self.route)

        assert response_[0] is not None
        assert response_[1].status_code == 201
        assert response_[1].reason == 'Created'

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")
