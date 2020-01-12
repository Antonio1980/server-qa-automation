import random
import allure
import pytest
from src.base.lib_ import logger
from src.base.lib_.slack import Slack
from config_definitions import BaseConfig
from src.base.entities.udp_message import UdpMessage
from src.base.lib_.log_decorator import automation_logger
from src.base.lib_.automation_error import AutomationError

test_case = "PROTO PER PORT"
BUFSIZ = 1024


@allure.feature("PROTOBUF")
@allure.story('Client able to ')
@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check (for every instance) that Location service response with protobuf on every provided port.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "protobuf_tests/check_proto_per_svc_port_test.py",
                 "TestProtobufPerServicePort")
@pytest.mark.liveness
class TestProtobufPerServicePort(object):
    first_case_issues = ""
    second_case_issues = ""
    latitude = 0.0
    longitude = 0.0
    bearing = random.uniform(0, 360)
    velocity = random.uniform(2, 40)
    accuracy = 5.0

    @automation_logger(logger)
    def test_endpoints_ports_with_protobuf(self, locations, socket_):
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
                        message1 = UdpMessage.get_udp_message_proto(self.latitude, self.longitude, self.bearing,
                                                                    self.velocity, self.accuracy)
                        message2 = UdpMessage.get_udp_message_proto(self.latitude, self.longitude, self.bearing,
                                                                    self.velocity, self.accuracy)
                        try:
                            socket_.udp_send(message1)

                            socket_.udp_send(message2)
                            _response = socket_.udp_receive(BUFSIZ)
                        except Exception as ex:
                            logger.logger.error(ex)
                            logger.logger.exception(f"{if_error}")
                            if tries != 2:
                                TestProtobufPerServicePort.second_case_issues += if_error
                            else:
                                error_ports.append(port)

                        if _response is not None:
                            logger.logger.info(
                                F"The instance {instance['instanceId']} is available for connect on port {port} !")
                            logger.logger.info(F"UDP Response: {_response}")

                if len(error_ports) > 0 and tries == 2:
                    logger.logger.info(f"!!! RECURSION !!! with next failed ports: {error_ports}")
                    check_ports(error_ports, tries - 1)

            check_ports(port_range)

        if TestProtobufPerServicePort.first_case_issues != "":
            logger.logger.info("---------- Those errors of the first test case will be sent to Slack Chanel ----------")
            logger.logger.fatal(f"{TestProtobufPerServicePort.first_case_issues}")
            Slack.send_message(TestProtobufPerServicePort.first_case_issues)

        if TestProtobufPerServicePort.second_case_issues != "":
            logger.logger.info("---------- Those errors of the second test case will be sent to Slack Chanel ---------")
            logger.logger.fatal(f"{TestProtobufPerServicePort.second_case_issues}")
            Slack.send_message(TestProtobufPerServicePort.second_case_issues)

            raise AutomationError(F"============ TEST CASE {test_case} FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
