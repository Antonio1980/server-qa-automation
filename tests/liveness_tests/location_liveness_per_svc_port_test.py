import random
import allure
import pytest
from src.common import logger
from src.common.utils.slack import Slack
from config_definitions import BaseConfig
from src.common.entities.udp_message import UdpMessage
from src.common.log_decorator import automation_logger
from src.common.automation_error import AutomationError

test_case = "LIVENESS PER PORT"
BUFSIZ = 1024


@allure.feature("LIVENESS")
@allure.story('Client able to found and connect to Location service via configured ports.')
@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that all running Location services returned in response "get endpoints" via Routing service.
    2. Check (for every instance) that Location service allows connections by provided ports.
    """)
@pytest.mark.usefixtures("run_time_counter", "endpoints", "socket_")
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "liveness_tests/location_liveness_per_svc_port_test.py",
                 "TestLocationLivenessPerServicePort")
@pytest.mark.liveness
class TestLocationLivenessPerServicePort(object):
    first_case_issues = ""
    second_case_issues = ""
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
            TestLocationLivenessPerServicePort.first_case_issues += if_err_message
            logger.logger.exception(if_err_message)

            raise AutomationError(if_err_message)
        else:
            logger.logger.info(F"Routing svc returned {len(endpoints)} endpoints -> PASSED !")

    @automation_logger(logger)
    def test_endpoints_ports(self, endpoints, socket_):
        allure.step("Verify that all provided ports are open and accept UDP connections.")

        for endpoint in endpoints:
            error_ports = []
            port_range = [p for p in range(endpoint["minPort"], endpoint["maxPort"] + 1)]
            logger.logger.info(F"Accepted ports are: {port_range}")

            def check_ports(ports, tries=2):
                if tries > 0:
                    for port in ports:
                        _response = None
                        socket_.udp_connect((endpoint["ip"], port))

                        if_error = F"The endpoint {endpoint['name']} is not responding on port {port} ! \n"
                        message1 = UdpMessage().get_udp_message(self.latitude, self.longitude, self.bearing,
                                                                self.velocity, self.accuracy)
                        message2 = UdpMessage().get_udp_message(self.latitude, self.longitude, self.bearing,
                                                                self.velocity, self.accuracy)
                        try:
                            socket_.udp_send(message1)

                            socket_.udp_send(message2)
                            _response = socket_.udp_receive(BUFSIZ)
                        except Exception:
                            logger.logger.exception(f"{if_error}")
                            if tries != 2:
                                TestLocationLivenessPerServicePort.second_case_issues += if_error
                            else:
                                error_ports.append(port)

                        if _response is not None:
                            logger.logger.info(
                                F"The endpoint {endpoint['name']} is available for connect on port {port} !")
                            logger.logger.info(F"UDP Response: {_response}")

                if len(error_ports) > 0 and tries == 2:
                    logger.logger.info(f"!!! RECURSION !!! with next failed ports: {error_ports}")
                    check_ports(error_ports, tries - 1)

            check_ports(port_range)

        if TestLocationLivenessPerServicePort.first_case_issues != "":
            logger.logger.info("---------- Those errors of the first test case will be sent to Slack Chanel ----------")
            logger.logger.fatal(f"{TestLocationLivenessPerServicePort.first_case_issues}")
            Slack.send_message(TestLocationLivenessPerServicePort.first_case_issues)

        if TestLocationLivenessPerServicePort.second_case_issues != "":
            logger.logger.info("---------- Those errors of the second test case will be sent to Slack Chanel ---------")
            logger.logger.fatal(f"{TestLocationLivenessPerServicePort.second_case_issues}")
            Slack.send_message(TestLocationLivenessPerServicePort.second_case_issues)

            raise AutomationError(F"============ TEST CASE {test_case} FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
