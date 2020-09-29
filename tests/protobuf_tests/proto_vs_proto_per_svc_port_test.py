import random
import allure
import pytest
from src.base.lib_ import logger
from src.base.lib_.slack import Slack
from config_definitions import BaseConfig
from src.base.entities.udp_message import UdpMessage
from src.base.lib_.log_decorator import automation_logger
from src.base.lib_.automation_error import AutomationError
from src.proto import LocationServiceResponse_pb2

test_case = "PROTO VS PROTO FOR EVERY PORT"
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
@pytest.mark.protobuf
class TestProtobufPerServicePort(object):
    test_case_issues = ""
    latitude = 0.1
    longitude = 0.1
    bearing = random.uniform(0, 360)
    velocity = random.uniform(2, 40)
    accuracy = 5.0

    @automation_logger(logger)
    def test_endpoints_ports_with_protobuf(self, locations, socket_):
        allure.step("Verify that all provided ports are open and accept UDP connections.")

        for instance in locations["instances"]:
            error_ports = []
            port_range = [p for p in range(instance["minPort"], instance["maxPort"] + 1)]
            logger.logger.info(F"Now testing instance: {instance['instanceId']}")
            logger.logger.info(F"Accepted ports are: {port_range}")

            def check_ports(ports, tries=2):
                if tries > 0:
                    for port in ports:
                        _response = None
                        socket_.udp_connect((instance["ip"], port))

                        if_error = F"The instance {instance['instanceId']} is not responding on port {port} ! \n"
                        message1 = UdpMessage().get_udp_message_proto(self.latitude, self.longitude, self.bearing,
                                                                    self.velocity, self.accuracy, "server-qa-automation-1")
                        message2 = UdpMessage().get_udp_message_proto(self.latitude, self.longitude, self.bearing,
                                                                    self.velocity, self.accuracy, "server-qa-automation-2")
                        try:
                            socket_.udp_send(message1)

                            socket_.udp_send(message2)
                            _response = socket_.udp_receive(BUFSIZ)
                        except Exception as ex:
                            logger.logger.error(ex)
                            logger.logger.exception(f"{if_error}")
                            if tries != 2:
                                TestProtobufPerServicePort.test_case_issues += if_error
                            else:
                                error_ports.append(port)

                        if isinstance(_response, bytes):
                            logger.logger.info(
                                F"The instance {instance['instanceId']} is available for connect on port {port} !")
                            proto_response = LocationServiceResponse_pb2.LocationServiceResponse()
                            proto_response.ParseFromString(_response)
                            logger.logger.info(F"UDP Response: {proto_response}")
                        elif _response is None:
                            logger.logger.warn(F"Response is None -> {_response}")
                        else:
                            TestProtobufPerServicePort.test_case_issues += F"The instance {instance['instanceId']} " \
                                                                           F"and port {port} returned not Proto! " \
                                                                           F"response is {_response}"

                if 0 < len(error_ports) < 10 and tries == 2:
                    logger.logger.info(f"!!! RECURSION !!! with next failed ports: {error_ports}")
                    check_ports(error_ports, tries - 1)

            check_ports(port_range)

        if TestProtobufPerServicePort.test_case_issues != "":
            logger.logger.info("---------- Those errors of the test case will be sent to Slack Chanel ---------")
            logger.logger.fatal(f"{TestProtobufPerServicePort.test_case_issues}")
            Slack.send_message(TestProtobufPerServicePort.test_case_issues)

            raise AutomationError(F"============ TEST CASE {test_case} FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
