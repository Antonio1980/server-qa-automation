import random
import allure
import pytest
from src.common import logger
from src.common.utils.slack import Slack
from config_definitions import BaseConfig
from src.common.udp_socket import UdpSocket
from src.common.entities.udp_message import UdpMessage
from src.common.log_decorator import automation_logger
from src.common.automation_error import AutomationError

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
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "tests/liveness_tests/location_liveness_per_svc_port_test.py",
                 "TestLocationLivenessPerServicePort")
@pytest.mark.liveness
class TestLocationLivenessPerServicePort(object):
    issues = ""
    latitude = "0.0"
    longitude = "0.0"
    bearing = random.uniform(0, 360)
    velocity = random.uniform(2, 40)
    accuracy = 5.0

    @automation_logger(logger)
    @allure.step("Verify that Routing svc returns all active endpoints.")
    def test_returned_endpoints(self, endpoints):
        ex_endpoints = int(BaseConfig.EXPECTED_ENDPOINTS)
        if_err_message = "Endpoints count != " + str(ex_endpoints) + " current number is " + str(len(endpoints)) + " \n"

        if len(endpoints) != ex_endpoints:
            TestLocationLivenessPerServicePort.issues += if_err_message
            logger.logger.exception(if_err_message)

            raise AutomationError(if_err_message)
        else:
            logger.logger.info(F"Routing svc returned {len(endpoints)} endpoints -> PASSED !")

    @automation_logger(logger)
    @allure.step("Verify that all provided ports are open and accept UDP connections.")
    def test_endpoints_ports(self, endpoints):
        count, port_range = 0, []
        for endpoint in endpoints:

            port_range = [p for p in range(endpoint["minPort"], endpoint["maxPort"] + 1)]
            logger.logger.info(F"Accepted ports are: {port_range}")

            for port in port_range:
                _socket = UdpSocket()
                _socket.udp_connect((endpoint["ip"], port))

                if_error = F"The endpoint {endpoint['name']} is not responding on port {port} ! \n"

                _socket.udp_send(UdpMessage().get_udp_message(self.latitude, self.longitude, self.bearing,
                                                              self.velocity, self.accuracy))

                _socket.udp_send(UdpMessage().get_udp_message(self.latitude, self.longitude, self.bearing,
                                                              self.velocity, self.accuracy))
                try:
                    response_ = _socket.udp_receive(BUFSIZ)
                except Exception as e:
                    response_ = None
                    if_data_error = F"Error occurred while receiving data: {e} \n"
                    logger.logger.exception(if_data_error)
                    TestLocationLivenessPerServicePort.issues += if_data_error
                if response_:
                    logger.logger.info(F"The endpoint {endpoint['name']} is available for connect on port {port} !")
                    logger.logger.info(F"UDP Response: {response_}")
                else:
                    TestLocationLivenessPerServicePort.issues += if_error
                    logger.logger.error(f"{if_error}")
                    count += 1

        if TestLocationLivenessPerServicePort.issues:
            logger.logger.fatal(f"{TestLocationLivenessPerServicePort.issues}")
            if count > int(((len(port_range) / 100) * 5)):
                Slack.send_message(TestLocationLivenessPerServicePort.issues)

            raise AutomationError(F"============ TEST CASE {test_case} FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
