import json
import random
import threading
import allure
import pytest
from google.protobuf.json_format import MessageToJson
from src.base.lib_ import logger
from src.base.lib_.slack import Slack
from config_definitions import BaseConfig
from src.base.entities.udp_message import UdpMessage
from src.base.lib_.log_decorator import automation_logger
from src.base.lib_.automation_error import AutomationError
from src.base.lib_.utils import Utils
from src.proto import LocationServiceResponse_pb2

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

    latitude = "0.1"
    longitude = "0.1"
    bearing = random.uniform(0, 360)
    velocity = random.uniform(2, 40)
    accuracy = 5.0

    @automation_logger(logger)
    def test_protobuf_fields(self, locations, socket_):
        allure.step("Verify that Protobuf message is correct.")
        issues = ""
        socket_.udp_connect((locations["instances"][0]["ip"], locations["instances"][0]["maxPort"]))
        id1, id2 = "server-qa-automation" + Utils.get_random_string(), "server-qa-automation" + Utils.get_random_string()
        if_error = F"The instance {locations['instances'][0]['instanceId']} is not responding on port " \
                   F"{locations['instances'][0]['maxPort']} ! \n"
        message1 = UdpMessage().get_udp_message(self.latitude, self.longitude, self.bearing,
                                                self.velocity, self.accuracy, id1)
        message2 = UdpMessage().get_udp_message_proto(0.1, 0.1, self.bearing, self.velocity, self.accuracy, id2)
        socket_.udp_send(message1)

        t1 = threading.Thread(target=socket_.udp_send(message2), args=[])
        t1.start()
        t1.join()

        response_ = socket_.udp_receive(BUFSIZ)

        if response_ is not None and isinstance(response_, bytes):
            logger.logger.warn(F"PURE Response: {response_}")
            logger.logger.info(
                F"The instance {locations['instances'][0]['instanceId']} available for connect on port "
                F"{locations['instances'][0]['maxPort']} !")
            proto_response = LocationServiceResponse_pb2.LocationServiceResponse()
            proto_response.ParseFromString(response_)
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
            assert "id" and "bearing" and "latitude" and "velocity" and "longitude" and "clientDataType" and "timestamp"\
                   "altitudeValue" and "horizontalAccuracy" and "verticalAccuracyValue" and "source" and \
                   "rawHorizontalAccuracyValue" in data_json.keys()
            assert data_json["id"] == id2
            assert data_json["bearing"] == self.bearing
            assert data_json["latitude"] == 0.1
            assert data_json["velocity"] == self.velocity
            assert data_json["longitude"] == 0.1
            assert data_json["clientDataType"] == "CAR"
            assert data_json["altitudeValue"] == 0.0
            assert data_json["horizontalAccuracy"] == self.accuracy
            assert data_json["verticalAccuracyValue"] == 0.0
            assert data_json["source"] == "QA Test"
            assert data_json["rawHorizontalAccuracyValue"] == 0.0
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
    def test_json_fields(self, locations, socket_):
        allure.step("Verify that Json message is correct.")
        issues = ""
        socket_.udp_connect((locations["instances"][0]["ip"], locations["instances"][0]["maxPort"]))
        id1, id2 = "server-qa-automation" + Utils.get_random_string(), "server-qa-automation" + Utils.get_random_string()
        if_error = F"The instance {locations['instances'][0]['instanceId']} is not responding on port " \
                   F"{locations['instances'][0]['maxPort']} ! \n"
        message1 = UdpMessage().get_udp_message_proto(1.1, 1.1, self.bearing, self.velocity, self.accuracy, id1)
        message2 = UdpMessage().get_udp_message("1.1", "1.1", self.bearing, self.velocity, self.accuracy, id2)
        socket_.udp_send(message1)

        t1 = threading.Thread(target=socket_.udp_send(message2), args=[])
        t1.start()
        t1.join()

        response_ = socket_.udp_receive(BUFSIZ)

        if response_ is not None and isinstance(response_, bytes):
            logger.logger.warn(F"PURE Response: {response_}")
            logger.logger.info(
                F"The instance {locations['instances'][0]['instanceId']} available for connect on port "
                F"{locations['instances'][0]['maxPort']} !")
            json_data = json.loads(response_)
            logger.logger.info(F"UDP Response: {json_data}")
            assert "type" and "toId" and "data" in json_data.keys()
            assert json_data["type"] == "LocationUpdate"
            assert json_data["toId"] == id1
            assert isinstance(json_data["data"], list)
            assert len(json_data["data"]) > 0
            assert isinstance(json_data["data"][0], dict)
            data_json = json_data["data"][0]
            assert "id" and "bearing" and "latitude" and "velocity" and "longitude" and "clientDataType" and "timestamp"\
                   "horizontalAccuracy" and "maxAcceleration" and "source" and "maxAngularChange" and "avgAcceleration" \
                   and "avgAngularChange" and "maxDeceleration" in data_json.keys()
            assert data_json["id"] == id2
            assert data_json["bearing"] == self.bearing
            assert data_json["latitude"] == 1.1
            assert data_json["velocity"] == self.velocity
            assert data_json["longitude"] == 1.1
            assert data_json["clientDataType"] == "CAR"
            assert data_json["horizontalAccuracy"] == self.accuracy
            assert data_json["source"] == "QA Test"
            assert data_json["maxAcceleration"] == 0.0
            assert data_json["maxAngularChange"] == 0.0
            assert data_json["avgAcceleration"] == 0.0
            assert data_json["avgAngularChange"] == 0.0
            assert data_json["maxDeceleration"] == 0.0
        else:
            issues += if_error
            logger.logger.error(f"{if_error}")

        if issues is not "":
            logger.logger.fatal(f"{issues}")
            # Slack.send_message(issues)

            raise AutomationError(F"============ TEST CASE {test_case} / 2 FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")
