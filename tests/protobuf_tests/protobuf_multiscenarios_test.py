import json
import random
import allure
import pytest
import threading
from src.base.lib_ import logger
from src.base.lib_.utils import Utils
from config_definitions import BaseConfig
from src.base.entities.udp_message import UdpMessage
from src.base.lib_.log_decorator import automation_logger
from src.base.lib_.automation_error import AutomationError
from src.proto import LocationServiceResponse_pb2
from src.base.instruments.udp_socket import UdpSocket

test_case = "PROTO/JSON SCENARIOS"
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

    j_latitude, p_latitude = "0.1", 0.1
    j_longitude, p_longitude = "0.1", 0.1
    bearing = random.uniform(0, 360)
    velocity = random.uniform(2, 40)
    max_port, min_port = "maxPort", "minPort"
    accuracy = 5.0
    issues1, issues2 = "", ""
    instance_1, instance_2 = 0, 1
    json_id1, proto_id1 = "server-qa-automation" + Utils.get_random_string(), "server-qa-automation" + \
                          Utils.get_random_string()
    json_id2, proto_id2 = "server-qa-automation" + Utils.get_random_string(), "server-qa-automation" + \
                          Utils.get_random_string()

    @automation_logger(logger)
    def test_client1_json_client2_protobuf(self, locations, socket_):
        allure.step("Verify that client2 received Protobuf.")
        ip_, port1, port2 = locations["instances"][self.instance_1]["ip"], \
                            locations["instances"][self.instance_1][self.min_port], \
                            locations["instances"][self.instance_1][self.max_port]
        socket_.udp_connect((ip_, port1))
        logger.logger.info(F"CONNECTED SOCKET JSON: {socket_.udp_socket.getsockname()}")
        er = F"Instance {locations['instances'][self.instance_1]['instanceId']} on port: {port1} failed to receive !\n"
        json_message = UdpMessage().get_udp_message(self.j_latitude, self.j_longitude, self.bearing, self.velocity,
                                                    self.accuracy, self.json_id1)
        socket_.udp_send(json_message)

        proto_thread = threading.Thread(target=self.send_proto_message(ip_, port2), daemon=True)
        proto_thread.start()

        response_ = socket_.udp_receive(BUFSIZ)

        if response_ is not None and isinstance(response_, bytes):
            logger.logger.warn(F"PURE Response: {response_}")
            logger.logger.info(F"UDP Response: {json.loads(response_)}")
        else:
            TestScenariosProtobuf.issues1 += er
            logger.logger.error(f"{er}")

        proto_thread.join()

        if TestScenariosProtobuf.issues1 is not "":
            logger.logger.fatal(f"{TestScenariosProtobuf.issues1}")

            raise AutomationError(F"============ TEST CASE {test_case} / 1 FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_client1_protobuf_client2_json(self, locations, socket_):
        allure.step("Verify that client2 received Json.")
        ip_, port1, port2 = locations["instances"][self.instance_2]["ip"], \
                            locations["instances"][self.instance_2][self.min_port], \
                            locations["instances"][self.instance_2][self.max_port]
        socket_.udp_connect((ip_, port1))

        er = F"Instance {locations['instances'][self.instance_2]['instanceId']} on port {port1} failed to receive !\n"
        proto_message = UdpMessage().get_udp_message_proto(self.p_latitude, self.p_longitude, self.bearing,
                                                           self.velocity, self.accuracy, self.proto_id2)
        socket_.udp_send(proto_message)

        json_thread = threading.Thread(target=self.send_json_message(ip_, port2), daemon=True)
        json_thread.start()

        response_ = socket_.udp_receive(BUFSIZ)

        if response_ is not None and isinstance(response_, bytes):
            logger.logger.warn(F"PURE Response: {response_}")
            proto_response = LocationServiceResponse_pb2.LocationServiceResponse()
            proto_response.ParseFromString(response_)
            logger.logger.info(F"UDP Response: {proto_response}")
        else:
            TestScenariosProtobuf.issues2 += er
            logger.logger.error(f"{er}")

        json_thread.join()

        if TestScenariosProtobuf.issues2 is not "":
            logger.logger.fatal(f"{TestScenariosProtobuf.issues2}")

            raise AutomationError(F"============ TEST CASE {test_case} / 2 FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def send_proto_message(self, _ip, port):
        allure.step("Send Protobuf message.")
        proto_socket = UdpSocket()
        proto_socket.udp_connect((_ip, port))
        logger.logger.info(F"IP {_ip} ready for connect on port {port} !")
        logger.logger.info(F"ANOTHER SOCKET PROTO : {proto_socket.udp_socket.getsockname()}")
        proto_message = UdpMessage().get_udp_message_proto(self.p_latitude, self.p_longitude, self.bearing,
                                                           self.velocity, self.accuracy, self.proto_id1)
        for i in range(5):
            proto_socket.udp_send(proto_message)

        return proto_socket.udp_socket.__exit__()

    @automation_logger(logger)
    def send_json_message(self, _ip, port):
        allure.step("Send Json message.")
        json_socket = UdpSocket()
        json_socket.udp_connect((_ip, port))
        logger.logger.info(F"IP {_ip} ready for connect on port {port} !")
        logger.logger.info(F"ANOTHER SOCKET JSON : {json_socket.udp_socket.getsockname()}")
        json_message = UdpMessage().get_udp_message(self.j_latitude, self.j_longitude, self.bearing, self.velocity,
                                                    self.accuracy, self.json_id2)
        for i in range(5):
            json_socket.udp_send(json_message)

        return json_socket.udp_socket.__exit__()

    @automation_logger(logger)
    def test_client1_json_client2_json(self, locations, socket_):
        allure.step("Verify that client1 and client2 received Json.")
        issues = ""
        for instance in locations["instances"]:
            port_range = [instance["minPort"], instance["maxPort"]]

            for port in port_range:
                socket_.udp_connect((instance["ip"], port))

                if_error = F"The instance {instance['instanceId']} is not responding on port {port} ! \n"
                message1 = UdpMessage().get_udp_message(self.j_latitude, self.j_longitude, self.bearing,
                                                        self.velocity, self.accuracy, "server-qa-automation-1")
                message2 = UdpMessage().get_udp_message(self.j_latitude, self.j_longitude, self.bearing,
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

            raise AutomationError(F"============ TEST CASE {test_case} / 3 FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
