import time
import allure
import pytest
from src.common import logger
from src.common.utils.slack import Slack
from src.common.log_decorator import automation_logger
from src.common.automation_error import AutomationError
from src.common.udp_socket import UdpSocket, UdpMessage

test_case = "liveness"
BUFSIZ = 1024


# @pytest.mark.incremental
@allure.feature('Location Service')
@allure.story('Client able to found and connect to Location service via configured ports.')
@allure.title("END TO END")
@allure.description("""
    Functional end to end test.
    1. Check that all running Location services returned in response "get endpoints" via Routing service.
    2. Check (for every instance) that Location service allows connections by provided ports.
    """)
@pytest.mark.usefixtures("run_time_count", "endpoints")
@allure.severity(allure.severity_level.BLOCKER)
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

    @automation_logger(logger)
    @pytest.mark.usefixtures("ex_endpoints")
    @allure.step("Verify that Routing svc returns all active endpoints.")
    def test_returned_endpoints(self, endpoints, ex_endpoints):
        if ex_endpoints is None:
            raise AutomationError("Environment variable 'EXPECTED_ENDPOINTS' is not provided...")

        if len(endpoints) != int(ex_endpoints):
            err_message = "Endpoints count != " + str(ex_endpoints) + "\n"
            TestLiveness.issues += err_message
            logger.logger.exception(err_message)
            raise AutomationError(err_message)
        else:
            logger.logger.info(F"Routing svc returned {len(endpoints)} endpoints -> PASSED !")

    @automation_logger(logger)
    @allure.step("Verify that all provided ports are open and accept UDP connections.")
    def test_endpoints_ports(self, endpoints):

        for endpoint in endpoints:

            UdpSocket.udp_send(self.message1, (endpoint["ip"], endpoint["minPort"]))
            UdpSocket.udp_send(self.message2, (endpoint["ip"], endpoint["maxPort"]))
            time.sleep(2.0)
            try:
                response_ = UdpSocket.udp_socket.recv(BUFSIZ)
                if response_:
                    logger.logger.info(F"The endpoint {endpoint['name']} is available for connect!  {response_}")
                else:
                    logger.logger.error(F"Not valid UDP response: {response_}")
            except Exception as e:
                error = F"The endpoint {endpoint['name']} is not responding! \n"
                TestLiveness.issues += error
                logger.logger.warning(f"{error}")
                logger.logger.exception(e)

        if TestLiveness.issues:
            logger.logger.warning(f"{TestLiveness.issues}")
            # Slack.send_message("IGNORE IT ===>" + TestLiveness.issues)
            raise AutomationError(F"============ TEST CASE {test_case} FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
