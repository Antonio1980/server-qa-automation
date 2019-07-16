import time
import allure
import pytest
from src.common import logger
from src.common.utils.slack import Slack
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger
from src.common.automation_error import AutomationError
from src.common.udp_socket import UdpSocket, UdpMessage

test_case = "liveness"


# @pytest.mark.incremental
@allure.feature('Location Service')
@allure.story('Client able to found and connect to Location service via configured ports.')
@allure.title("END TO END")
@allure.description("""
    Functional end to end test.
    1. Check that all running Location services returned in response "get endpoints" via Routing service.
    2. Check (for every instance) that Location service allows connections by provided ports.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase("TestLiveness")
@pytest.mark.regression
@pytest.mark.routing_service
class TestLiveness(object):
    issues = ""
    latitude = "0.0"
    longitude = "0.0"
    bearing = 0
    velocity = 0
    accuracy = 5.0

    message1 = UdpMessage().udp_message(latitude, longitude, bearing, velocity, accuracy).encode()
    message2 = UdpMessage().udp_message(latitude, longitude, bearing, velocity, accuracy).encode()

    @pytest.fixture(scope="class")
    @automation_logger(logger)
    def endpoints(self):
        response_ = ApiClient().routing_svc.get_endpoints()
        return response_

    @automation_logger(logger)
    @allure.step(F"Verify that Routing svc returns all active endpoints.")
    def test_returned_endpoints(self, endpoints):
        if len(endpoints) != 2:
            err_message = "Endpoints count != " + str(2) + "\n"
            TestLiveness.issues += err_message
            logger.logger.exception(err_message)
            raise AutomationError(err_message)
        else:
            logger.logger.info(F"Routing svc returned {len(endpoints)} endpoints -> PASSED !")

    @automation_logger(logger)
    @allure.step(F"Verify that all provided ports are open and accept UDP connections.")
    def test_endpoints_ports(self, endpoints):

        for endpoint in endpoints:

            UdpSocket.udp_send(self.message1, (endpoint["ip"], endpoint["minPort"]))
            UdpSocket.udp_send(self.message2, (endpoint["ip"], endpoint["maxPort"]))
            time.sleep(1.0)
            try:
                response_ = UdpSocket.udp_socket.recv(10000)
                if response_:
                    logger.logger.info(F"The endpoint {endpoint['name']} is available for connect!")
                else:
                    logger.logger.error(F"The endpoint {endpoint['name']} is not available!")
            except Exception as e:
                error = F"The endpoint {endpoint['name']} is not responding! \n"
                TestLiveness.issues += error
                logger.logger.exception(error, e)

        if TestLiveness.issues:
            logger.logger.warning(f"{TestLiveness.issues}")
            Slack.send_message("IGNORE IT ===>" + TestLiveness.issues)
            raise AutomationError(F"============ TEST CASE {test_case} FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
