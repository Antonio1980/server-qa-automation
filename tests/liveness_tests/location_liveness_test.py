import random
import allure
import pytest
from src.common.utils import logger
from src.common.utils.slack import Slack
from config_definitions import BaseConfig
from src.common.entities.udp_message import UdpMessage
from src.common.utils.log_decorator import automation_logger
from src.common.automation_error import AutomationError

test_case = "LIVENESS LOCATION"
BUFSIZ = 1024


@pytest.mark.skip
@allure.feature("LIVENESS")
@allure.story('Client able to found and connect to Location service via min and max ports.')
@allure.title(test_case)
@allure.description("""
    Functional end to end test.
    1. Check that all running Location services returned in response "get endpoints" via Routing service.
    2. Check (for every instance) that Location service allows connections by provided min/max ports.
    """)
@pytest.mark.usefixtures("endpoints", "socket_")
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "liveness_tests/location_liveness_test.py", "TestLiveness")
@pytest.mark.liveness
class TestLiveness(object):
    issues = ""
    latitude = "0.0"
    longitude = "0.0"
    bearing = random.uniform(0, 360)
    velocity = random.uniform(2, 40)
    accuracy = 5.0

    @automation_logger(logger)
    def test_returned_endpoints(self, endpoints):
        allure.step("Verify that Routing svc returns all active endpoints.")

        ex_endpoints = int(BaseConfig.EXPECTED_ENDPOINTS)
        if_err_message = "Endpoints count != " + str(ex_endpoints) + " current number is " + str(len(endpoints)) + " \n"

        if len(endpoints) != ex_endpoints:
            TestLiveness.issues += if_err_message
            logger.logger.exception(if_err_message)

            raise AutomationError(if_err_message)
        else:
            logger.logger.info(F"Routing svc returned {len(endpoints)} endpoints -> PASSED !")

    @automation_logger(logger)
    def test_endpoints_ports(self, endpoints, socket_):
        allure.step("Verify that all provided ports are open and accept UDP connections.")

        for endpoint in endpoints:
            port_range = [endpoint["minPort"], endpoint["maxPort"]]

            for port in port_range:
                socket_.udp_connect((endpoint["ip"], port))

                if_error = F"The endpoint {endpoint['name']} is not responding on port {port} ! \n"
                message1 = UdpMessage().get_udp_message(self.latitude, self.longitude, self.bearing,
                                                        self.velocity, self.accuracy)
                message2 = UdpMessage().get_udp_message(self.latitude, self.longitude, self.bearing,
                                                        self.velocity, self.accuracy)
                try:
                    socket_.udp_send(message1)

                    socket_.udp_send(message2)
                    response_ = socket_.udp_receive(BUFSIZ)
                except Exception as e:
                    response_ = None
                    if_data_error = F"Error occurred while receiving data: {e} \n"
                    logger.logger.exception(if_data_error)
                    TestLiveness.issues += if_data_error
                if response_:
                    logger.logger.info(F"The endpoint {endpoint['name']} is available for connect on port {port} !")
                    logger.logger.info(F"UDP Response: {response_}")
                else:
                    TestLiveness.issues += if_error
                    logger.logger.error(f"{if_error}")

        if TestLiveness.issues:
            logger.logger.fatal(f"{TestLiveness.issues}")
            Slack.send_message(TestLiveness.issues)

            raise AutomationError(F"============ TEST CASE {test_case} FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
