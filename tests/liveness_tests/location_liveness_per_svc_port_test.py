import json
import random
import allure
import pytest
from src.base.lib_ import logger
from src.base.lib_.slack import Slack
from config_definitions import BaseConfig
from src.base.entities.udp_message import UdpMessage
from src.base.lib_.log_decorator import automation_logger
from src.base.lib_.automation_error import AutomationError

test_case = "LIVENESS LOCATION PER PORT"
BUFSIZ = 1024


@allure.feature("LIVENESS")
@allure.story('Client able to found and connect to Location service via configured ports.')
@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that number of Location definition returned in response "get_location_services_v1" equals to number of instances.
    2. Check (for every instance) that Location service allows connections by provided ports.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "protobuf_tests/proto_vs_proto_per_svc_port_test.py",
                 "TestLivenessPerServicePort")
@pytest.mark.liveness
class TestLivenessPerServicePort(object):
    first_case_issues = ""
    second_case_issues = ""
    latitude = "0.1"
    longitude = "0.1"
    bearing = random.uniform(0, 360)
    velocity = random.uniform(2, 40)
    accuracy = 5.0

    @automation_logger(logger)
    def test_returned_endpoints(self, locations):
        allure.step("Verify that Routing svc sum of returned location definitions equals to sum returned instances. ")

        definitions_len, instances_len = len(locations["definitions"]), len(locations["instances"])
        if_err_message = f"Definitions count {definitions_len} != number of instances {instances_len}"

        if definitions_len != instances_len:
            TestLivenessPerServicePort.first_case_issues += if_err_message
            logger.logger.exception(if_err_message)

            raise AutomationError(if_err_message)
        else:
            logger.logger.info(F"Routing svc returned {definitions_len} endpoints -> PASSED !")

    @automation_logger(logger)
    def test_endpoints_ports(self, locations, socket_):
        allure.step("Verify that all provided ports are open and accept UDP connections.")

        for instance in locations["instances"]:
            error_ports = []
            port_range = [p for p in range(instance["minPort"], instance["maxPort"] + 1)]
            logger.logger.info(F"Accepted ports are: {port_range}")

            def check_ports(ports, tries=2):
                if tries > 0:
                    for port in ports:
                        _response = None
                        socket_.udp_connect((instance["ip"], port))

                        if_error = F"The instance {instance['instanceId']} is not responding on port {port} ! \n"
                        message1 = UdpMessage().get_udp_message(self.latitude, self.longitude, self.bearing,
                                                                self.velocity, self.accuracy, "server-qa-automation-1")
                        message2 = UdpMessage().get_udp_message(self.latitude, self.longitude, self.bearing,
                                                                self.velocity, self.accuracy, "server-qa-automation-2")
                        try:
                            socket_.udp_send(message1)

                            socket_.udp_send(message2)
                            _response = socket_.udp_receive(BUFSIZ)
                        except Exception as ex:
                            logger.logger.error(ex)
                            logger.logger.exception(f"{if_error}")
                            if tries != 2:
                                TestLivenessPerServicePort.second_case_issues += if_error
                            else:
                                error_ports.append(port)

                        if _response is not None:
                            logger.logger.info(
                                F"The instance {instance['instanceId']} is available for connect on port {port} !")
                            logger.logger.info(F"UDP Response: {json.loads(_response)}")

                if len(error_ports) > 0 and tries == 2:
                    logger.logger.info(f"!!! RECURSION !!! with next failed ports: {error_ports}")
                    check_ports(error_ports, tries - 1)

            check_ports(port_range)

        if TestLivenessPerServicePort.first_case_issues is not "":
            logger.logger.info("---------- Those errors of the first test case will be sent to Slack Chanel ----------")
            logger.logger.fatal(f"{TestLivenessPerServicePort.first_case_issues}")
            Slack.send_message(TestLivenessPerServicePort.first_case_issues)

        if TestLivenessPerServicePort.second_case_issues != "":
            logger.logger.info("---------- Those errors of the second test case will be sent to Slack Chanel ---------")
            logger.logger.fatal(f"{TestLivenessPerServicePort.second_case_issues}")
            Slack.send_message(TestLivenessPerServicePort.second_case_issues)

            raise AutomationError(F"============ TEST CASE {test_case} FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
