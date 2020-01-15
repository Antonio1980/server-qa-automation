import json
import time
import random
import allure
import pytest
import threading
from src.base.lib_ import logger
from src.base.lib_.utils import Utils
from config_definitions import BaseConfig
from google.protobuf.message import DecodeError
from src.proto import LocationServiceResponse_pb2
from src.base.entities.udp_message import UdpMessage
from google.protobuf.json_format import MessageToJson
from src.base.lib_.log_decorator import automation_logger
from src.base.lib_.automation_error import AutomationError
from src.base.instruments.udp_socket import UdpSocket, timeout

test_case = "PROTO CONTENT"
BUFSIZ = 1024


@allure.feature("PROTOBUF")
@allure.story('Client should received UDP messages with valid fields format accordingly.')
@allure.title(test_case)
@allure.description("""
    Functional end to end tests.
    1. Check content of protobuf message.
    2. Check content of json message.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "protobuf_tests/protobuf_and_json_fields_test.py", "TestProtobufAndJsonFields")
@pytest.mark.liveness
@pytest.mark.protobuf
class TestProtobufAndJsonFields(object):

    latitude1, latitude2 = "0.1", 0.1
    longitude1, longitude2 = "0.1", 0.1
    bearing = random.uniform(0, 360)
    velocity = random.uniform(2, 40)
    port1, port2 = "maxPort", "minPort"
    accuracy = 5.0
    issues1, issues2 = "", ""
    json_id1, proto_id1 = "server-qa-automation" + Utils.get_random_string(), "server-qa-automation" + \
                          Utils.get_random_string()
    json_id2, proto_id2 = "server-qa-automation" + Utils.get_random_string(), "server-qa-automation" + \
                          Utils.get_random_string()

    @automation_logger(logger)
    def test_protobuf_fields(self, locations, socket_):
        allure.step("Verify that Protobuf message is correct.")
        json_socket = socket_
        try:
            json_socket.udp_connect((locations["instances"][0]["ip"], locations["instances"][0][self.port1]))
            logger.logger.info(F"SOCKET JSON: {json_socket.udp_socket.getsockname()}")
        except Exception as e:
            logger.logger.error(F"The instance {locations['instances'][0]['instanceId']} is not responding on port "
                                F"{locations['instances'][0][self.port1]} ! \n")
            TestProtobufAndJsonFields.issues1 += "Unable to connect."
            raise AutomationError(e.args)

        json_message = UdpMessage().get_udp_message(self.latitude1, self.longitude1, self.bearing, self.velocity,
                                                    self.accuracy, self.json_id1)
        json_socket.udp_send(json_message)

        t1 = threading.Thread(target=self.send_proto_message(locations), daemon=True)
        t1.start()
        t1.join()

        res, response_ = False, None
        start_time = time.perf_counter()
        while not res and time.perf_counter() < start_time + 10.0:
            try:
                response_ = json_socket.udp_receive(BUFSIZ)
                logger.logger.info(F"SOCKET JSON: {json_socket.udp_socket.getsockname()}")
                logger.logger.warn(F"PURE Response: {response_}")
                res = True
                if isinstance(response_, bytes):
                    self.check_response_proto(response_)
            except timeout as te:
                logger.logger.error(F"WHILE {te}")

        if response_ is None or not isinstance(response_, bytes):
            TestProtobufAndJsonFields.issues1 += "send_message failed."
            raise AutomationError("send_proto_message Thread failed.")

        if TestProtobufAndJsonFields.issues1 is not "":
            logger.logger.fatal(f"{TestProtobufAndJsonFields.issues1}")

            raise AutomationError(F"============ TEST CASE {test_case} / 1 FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_json_fields(self, locations, socket_):
        allure.step("Verify that Json message is correct.")
        proto_socket = socket_
        try:
            proto_socket.udp_connect((locations["instances"][0]["ip"], locations["instances"][0][self.port1]))
            logger.logger.info(F"SOCKET PROTO : {proto_socket.udp_socket.getsockname()}")
        except Exception as e:
            logger.logger.error(F"The instance {locations['instances'][0]['instanceId']} is not responding on port "
                                F"{locations['instances'][0][self.port1]} ! \n")
            TestProtobufAndJsonFields.issues2 += "Unable to connect."
            raise AutomationError(e.args)

        proto_message = UdpMessage().get_udp_message_proto(self.latitude2, self.longitude2, self.bearing,
                                                           self.velocity, self.accuracy, self.json_id2)
        for i in range(5):
            proto_socket.udp_send(proto_message)

        t1 = threading.Thread(target=self.send_json_message(locations), daemon=True)
        t1.start()
        t1.join()

        res, response_ = False, None
        start_time = time.perf_counter()
        while not res and time.perf_counter() < start_time + 10.0:
            try:
                response_ = proto_socket.udp_receive(BUFSIZ)
                logger.logger.warn(F"PURE Response: {response_}")
                res = True
                if isinstance(response_, bytes):
                    self.check_response_json(response_)
            except timeout as te:
                logger.logger.error(F"WHILE {te}")

        if response_ is None or not isinstance(response_, bytes):
            TestProtobufAndJsonFields.issues1 += "send_message failed."
            raise AutomationError("send_json_message Thread failed.")

        if TestProtobufAndJsonFields.issues2 is not "":
            logger.logger.fatal(f"{TestProtobufAndJsonFields.issues2}")

            raise AutomationError(F"============ TEST CASE {test_case} / 2 FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def check_response_proto(self, response_):
        if response_ is not None and isinstance(response_, bytes):
            proto_response = LocationServiceResponse_pb2.LocationServiceResponse()
            try:
                proto_response.ParseFromString(response_)
            except DecodeError as dr:
                TestProtobufAndJsonFields.issues1 += "Response different from proto."
                logger.logger.error(f"{TestProtobufAndJsonFields.issues1}")
                raise AutomationError(dr.args)
            logger.logger.info(F"UDP Response: {proto_response}")
            proto_json = json.loads(MessageToJson(proto_response, including_default_value_fields=False))
            assert isinstance(proto_json["serverLocationsData"], dict)
            assert "clientDatas" in proto_json["serverLocationsData"].keys()
            assert isinstance(proto_json["serverLocationsData"]["clientDatas"], dict)
            assert "data" in proto_json["serverLocationsData"]["clientDatas"].keys()
            assert isinstance(proto_json["serverLocationsData"]["clientDatas"]["data"], list)
            assert len(proto_json["serverLocationsData"]["clientDatas"]["data"]) > 0
            assert isinstance(proto_json["serverLocationsData"]["clientDatas"]["data"][0], dict)
            data_json = proto_json["serverLocationsData"]["clientDatas"]["data"][0]
            assert "id" and "bearing" and "latitude" and "velocity" and "longitude" and "clientDataType" and \
                   "timestamp" and "altitudeValue" and "horizontalAccuracy" and "verticalAccuracyValue" and \
                   "source" and "rawHorizontalAccuracyValue" in data_json.keys()
            assert data_json["id"] == self.proto_id1
            assert data_json["bearing"] == self.bearing
            assert data_json["latitude"] == self.latitude2
            assert data_json["velocity"] == self.velocity
            assert data_json["longitude"] == self.longitude2
            assert data_json["horizontalAccuracy"] == self.accuracy
            assert data_json["source"] == "QA Test"
            assert data_json["clientDataType"] == "CAR"
            assert data_json["altitudeValue"] == 0.0
            assert data_json["verticalAccuracyValue"] == 0.0
            assert data_json["rawHorizontalAccuracyValue"] == 0.0
        else:
            TestProtobufAndJsonFields.issues1 += "Response is None"
            logger.logger.error(f"{TestProtobufAndJsonFields.issues1}")

    @automation_logger(logger)
    def check_response_json(self, response_):
        if response_ is not None:
            json_data = json.loads(response_)
            logger.logger.info(F"UDP Response: {json_data}")
            assert "type" and "toId" and "data" in json_data.keys()
            assert json_data["type"] == "LocationUpdate"
            assert json_data["toId"] == self.json_id2
            assert isinstance(json_data["data"], list)
            assert len(json_data["data"]) > 0
            assert isinstance(json_data["data"][0], dict)
            data_json = json_data["data"][0]
            assert "id" and "bearing" and "latitude" and "velocity" and "longitude" and "clientDataType" and \
                   "timestamp" and "horizontalAccuracy" and "maxAcceleration" and "source" and "maxAngularChange" and \
                   "avgAcceleration" and "avgAngularChange" and "maxDeceleration" in data_json.keys()
            assert data_json["id"] == self.proto_id2
            assert data_json["bearing"] == self.bearing
            assert data_json["latitude"] == self.latitude2
            assert data_json["velocity"] == self.velocity
            assert data_json["longitude"] == self.longitude2
            assert data_json["clientDataType"] == "CAR"
            assert data_json["horizontalAccuracy"] == self.accuracy
            assert data_json["source"] == "QA Test"
            assert data_json["maxAcceleration"] == 0.0
            assert data_json["maxAngularChange"] == 0.0
            assert data_json["avgAcceleration"] == 0.0
            assert data_json["avgAngularChange"] == 0.0
            assert data_json["maxDeceleration"] == 0.0
        else:
            TestProtobufAndJsonFields.issues2 += "Response is None"
            logger.logger.error(f"{TestProtobufAndJsonFields.issues2}")

    @automation_logger(logger)
    def send_proto_message(self, locations):
        proto_socket = UdpSocket()
        proto_socket.udp_connect((locations["instances"][0]["ip"], locations["instances"][0][self.port2]))
        logger.logger.info(F"SOCKET PROTO : {proto_socket.udp_socket.getsockname()}")
        proto_message = UdpMessage().get_udp_message_proto(self.latitude2, self.longitude2, self.bearing,
                                                           self.velocity, self.accuracy, self.proto_id1)
        # time.sleep(0.5)
        for i in range(5):
            proto_socket.udp_send(proto_message)

    @automation_logger(logger)
    def send_json_message(self, locations):
        json_socket = UdpSocket()
        json_socket.udp_connect((locations["instances"][0]["ip"], locations["instances"][0][self.port2]))
        logger.logger.info(F"SOCKET JSON : {json_socket.udp_socket.getsockname()}")
        json_message = UdpMessage().get_udp_message(self.latitude1, self.longitude1, self.bearing, self.velocity,
                                                    self.accuracy, self.proto_id2)
        time.sleep(0.5)
        for i in range(5):
            json_socket.udp_send(json_message)
