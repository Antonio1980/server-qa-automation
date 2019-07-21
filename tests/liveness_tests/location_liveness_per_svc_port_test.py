import allure
import pytest
from src.common import logger
from src.common.utils.slack import Slack
from config_definitions import BaseConfig
from src.common.log_decorator import automation_logger
from src.common.automation_error import AutomationError
from src.common.udp_socket import UdpSocket, UdpMessage

test_case = "location_liveness"
BUFSIZ = 1024


@allure.feature('Liveness')
@allure.story('Client able to found and connect to Location service via configured ports.')
@allure.title("Location Service")
@allure.description("""
    Functional test.
    1. Check that all running Location services returned in response "get endpoints" via Routing service.
    2. Check (for every instance) that Location service allows connections by provided ports.
    """)
@pytest.mark.usefixtures("run_time_count", "endpoints")
@allure.severity(allure.severity_level.MINOR)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/liveness_tests/location_liveness_per_svc_port_test.py", "TestLivenessPerServicePort")
@pytest.mark.liveness
class TestLocationLivenessPerServicePort(object):
    issues = ""
    latitude = "0.0"
    longitude = "0.0"
    bearing = 0
    velocity = 0
    accuracy = 5.0

    message1 = UdpMessage().set_udp_message(latitude, longitude, bearing, velocity, accuracy).encode()
    message2 = UdpMessage().set_udp_message(latitude, longitude, bearing, velocity, accuracy).encode()

    @automation_logger(logger)
    # @pytest.mark.usefixtures("ex_endpoints")
    @allure.step("Verify that Routing svc returns all active endpoints.")
    def test_returned_endpoints(self, endpoints):
        ex_endpoints = int(BaseConfig.EXPECTED_ENDPOINTS)
        # if ex_endpoints is None:
        #     raise AutomationError("Environment variable 'EXPECTED_ENDPOINTS' is not provided...")

        if len(endpoints) != ex_endpoints:
            err_message = "Endpoints count != " + str(ex_endpoints) + "\n"
            TestLocationLivenessPerServicePort.issues += err_message
            logger.logger.exception(err_message)
            raise AutomationError(err_message)
        else:
            logger.logger.info(F"Routing svc returned {len(endpoints)} endpoints -> PASSED !")

    @automation_logger(logger)
    @allure.step("Verify that all provided ports are open and accept UDP connections.")
    def test_endpoints_ports(self, endpoints):

        for endpoint in endpoints:

            port_range = [p for p in range(endpoint["minPort"], endpoint["maxPort"] + 1)]
            logger.logger.info(F"Accepted ports are: {port_range}")

            for port in port_range:
                if_error = F"The endpoint {endpoint['name']} is not responding on port {port} ! \n"

                UdpSocket.udp_send(self.message1, (endpoint["ip"], port))
                UdpSocket.udp_send(self.message2, (endpoint["ip"], port))

                try:
                    response_ = UdpSocket.udp_socket.recv(BUFSIZ)
                    if response_:
                        logger.logger.info(F"The endpoint {endpoint['name']} is available for connect on port {port} !")
                        logger.logger.info(F"UDP Response: {response_}")
                    else:
                        logger.logger.error(f"{if_error}")
                except Exception as e:
                    TestLocationLivenessPerServicePort.issues += if_error
                    logger.logger.error(f"{if_error}")
                    logger.logger.exception(e)

        if TestLocationLivenessPerServicePort.issues:
            logger.logger.fatal(f"{TestLocationLivenessPerServicePort.issues}")
            Slack.send_message(TestLocationLivenessPerServicePort.issues)
            raise AutomationError(F"============ TEST CASE {test_case} FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
