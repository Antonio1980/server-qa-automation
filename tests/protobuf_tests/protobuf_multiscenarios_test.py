import json
import random
import threading
import allure
import pytest
from src.base.lib_ import logger
from src.base.lib_.slack import Slack
from config_definitions import BaseConfig
from src.base.entities.udp_message import UdpMessage
from src.base.lib_.log_decorator import automation_logger
from src.base.lib_.automation_error import AutomationError
from src.base.lib_.utils import Utils
from src.proto import LocationServiceResponse_pb2

test_case = "PROTO SCENARIOS"
BUFSIZ = 1024


@allure.feature("PROTOBUF")
@allure.story('Client able to received UDP messages according to format in which it was sent.')
@allure.title(test_case)
@allure.description("""
    Functional end to end tests.
    1. Check that if client1 sends json and client2 sends proto then client2 receives proto.
    2. Check that if client1 sends proto and client2 sends json then client2 receives json.
    3. Check that if client1 sends json and client2 sends json then client2 and client1 receives json.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "protobuf_tests/protobuf_multiscenarios_test.py", "TestScenariosProtobuf")
@pytest.mark.liveness
@pytest.mark.protobuf
class TestScenariosProtobuf(object):

    latitude = "0.1"
    longitude = "0.1"
    bearing = random.uniform(0, 360)
    velocity = random.uniform(2, 40)
    accuracy = 5.0

    @automation_logger(logger)
    def test_client1_json_client2_protobuf(self, locations, socket_):
        allure.step("Verify that client2 received Protobuf.")
        issues = ""
        socket_.udp_connect((locations["instances"][0]["ip"], locations["instances"][0]["minPort"]))

        if_error = F"The instance {locations['instances'][0]['instanceId']} is not responding on port " \
                   F"{locations['instances'][0]['minPort']} ! \n"
        message1 = UdpMessage().get_udp_message(self.latitude, self.longitude, self.bearing, self.velocity,
                                                self.accuracy, "server-qa-automation" + Utils.get_random_string())
        message2 = UdpMessage().get_udp_message_proto(0.1, 0.1, self.bearing, self.velocity, self.accuracy,
                                                      "server-qa-automation" + Utils.get_random_string())
        socket_.udp_send(message1)

        def send_message():
            for i in range(6):
                socket_.udp_send(message2)
            return socket_

        t1 = threading.Thread(target=send_message, daemon=True)
        t1.start()
        t1.join()

        response_ = socket_.udp_receive(BUFSIZ)

        if response_ is not None and isinstance(response_, bytes):
            logger.logger.warn(F"PURE Response: {response_}")
            logger.logger.info(
                F"The instance {locations['instances'][0]['instanceId']} available for connect on port "
                F"{locations['instances'][0]['minPort']} !")
            proto_response = LocationServiceResponse_pb2.LocationServiceResponse()
            proto_response.ParseFromString(response_)
            logger.logger.info(F"UDP Response: {proto_response}")
        else:
            issues += if_error
            logger.logger.error(f"{if_error}")

        if issues is not "":
            logger.logger.fatal(f"{issues}")
            # Slack.send_message(issues)

            raise AutomationError(F"============ TEST CASE {test_case} / 1 FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_client1_protobuf_client2_json(self, locations, socket_):
        allure.step("Verify that client2 received Json.")
        issues = ""
        socket_.udp_connect((locations["instances"][0]["ip"], locations["instances"][0]["maxPort"]))

        if_error = F"The instance {locations['instances'][0]['instanceId']} is not responding on port " \
                   F"{locations['instances'][0]['maxPort']} ! \n"
        message1 = UdpMessage().get_udp_message_proto(1.1, 1.1, self.bearing, self.velocity, self.accuracy,
                                                      "server-qa-automation" + Utils.get_random_string())
        message2 = UdpMessage().get_udp_message("1.1", "1.1", self.bearing, self.velocity, self.accuracy,
                                                "server-qa-automation" + Utils.get_random_string())
        socket_.udp_send(message1)

        def send_message():
            socket_.udp_send(message2)
            return socket_

        t1 = threading.Thread(target=send_message, daemon=True)
        t1.start()
        t1.join()

        response_ = socket_.udp_receive(BUFSIZ)

        if response_ is not None and isinstance(response_, bytes):
            logger.logger.warn(F"PURE Response: {response_}")
            logger.logger.info(
                F"The instance {locations['instances'][0]['instanceId']} available for connect on port "
                F"{locations['instances'][0]['maxPort']} !")
            logger.logger.info(F"UDP Response: {json.loads(response_)}")
        else:
            issues += if_error
            logger.logger.error(f"{if_error}")

        if issues is not "":
            logger.logger.fatal(f"{issues}")
            # Slack.send_message(issues)

            raise AutomationError(F"============ TEST CASE {test_case} / 2 FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_client1_json_client2_json(self, locations, socket_):
        allure.step("Verify that client1 and client2 received Json.")
        issues = ""
        for instance in locations["instances"]:
            port_range = [instance["minPort"], instance["maxPort"]]

            for port in port_range:
                socket_.udp_connect((instance["ip"], port))

                if_error = F"The instance {instance['instanceId']} is not responding on port {port} ! \n"
                message1 = UdpMessage().get_udp_message(self.latitude, self.longitude, self.bearing,
                                                        self.velocity, self.accuracy, "server-qa-automation-1")
                message2 = UdpMessage().get_udp_message(self.latitude, self.longitude, self.bearing,
                                                        self.velocity, self.accuracy, "server-qa-automation-2")
                try:
                    socket_.udp_send(message1)
                    socket_.udp_send(message2)
                    response_ = socket_.udp_receive(BUFSIZ)
                except Exception as ex:
                    response_ = None
                    if_data_error = F"Error occurred while receiving data: {ex} \n"
                    logger.logger.exception(if_data_error)
                    issues += if_data_error
                if response_:
                    logger.logger.info(F"The instance {instance['instanceId']} available for connect on port {port} !")
                    logger.logger.info(F"UDP Response: {json.loads(response_)}")
                else:
                    issues += if_error
                    logger.logger.error(f"{if_error}")

        if issues is not "":
            logger.logger.fatal(f"{issues}")
            # Slack.send_message(issues)

            raise AutomationError(F"============ TEST CASE {test_case} / 3 FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
