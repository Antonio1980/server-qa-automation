import allure
import pytest
from src.common import logger
from src.common.log_decorator import automation_logger

test_case = ""


@allure.testcase("TestGetEndpoints")
@pytest.mark.regression
@pytest.mark.routing_service
class TestGetEndpoints(object):

    @automation_logger(logger)
    def test_get_endpoints_method_works(self):
        pass