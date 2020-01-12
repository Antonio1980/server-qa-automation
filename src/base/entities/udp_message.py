import random

from src.base.lib_ import logger
from src.base.entities.entity import Entity
from src.base.lib_.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.lib_.utils import Utils
from src.proto import LocationServiceRequest_pb2, ClientData_pb2


class UdpMessage(Entity):
    def __init__(self, debug_mode=True):
        super(UdpMessage, self).__init__()
        self.type = "LocationUpdate3"
        self.data = dict()
        self.data[DEBUG_MODE] = debug_mode

    @automation_logger(logger)
    def get_udp_message(self, *args):
        """
        Builds UDP message with dictionary structure.
        :param args: latitude- str, longitude- str, bearing- int (0-1), velocity- int (0-1), accuracy- float
        :return: Request body as python object UdpMessage().
        """
        (latitude, longitude, bearing, velocity, accuracy) = args
        self.data[CLIENT_DATA] = dict()
        self.data[CLIENT_DATA][TIMESTAMP] = Utils.get_times()
        self.data[CLIENT_DATA][ID] = "server-qa-automation"
        self.data[CLIENT_DATA][CLIENT_DATA_TYPE] = DetectedType.CAR.value
        self.data[CLIENT_DATA][LATITUDE] = str(latitude)
        self.data[CLIENT_DATA][LONGITUDE] = str(longitude)
        self.data[CLIENT_DATA][BEARING] = bearing
        self.data[CLIENT_DATA][VELOCITY] = velocity
        self.data[CLIENT_DATA][HORIZONTAL_ACCURACY] = float(accuracy)
        self.data[CLIENT_DATA][SOURCE] = "QA Test"
        logger.logger.info(F"UDP Message is {self.to_json()}")
        return Utils.to_json_dumps(self).encode("utf8")

    @staticmethod
    @automation_logger(logger)
    def get_udp_message_proto(*args):
        (latitude, longitude, bearing, velocity, accuracy) = args
        request = LocationServiceRequest_pb2.LocationServiceRequest()
        request.type = LocationServiceRequest_pb2.LocationServiceRequest.CLIENT_LOCATION

        request.clientLocationData.debugMode = False
        request.clientLocationData.notifyMe = True
        request.clientLocationData.notifyOthers = True
        request.clientLocationData.clientData.id = "server-qa-automation"
        request.clientLocationData.clientData.clientDataType = ClientData_pb2.ClientData.CAR
        request.clientLocationData.clientData.latitude = latitude
        request.clientLocationData.clientData.longitude = longitude
        request.clientLocationData.clientData.bearing = bearing
        request.clientLocationData.clientData.velocity = velocity
        request.clientLocationData.clientData.horizontalAccuracy = accuracy
        request.clientLocationData.clientData.timestamp = Utils.get_timestamps()[1]
        request.clientLocationData.clientData.source = "QA Test"
        data_bytes = request.SerializeToString()
        logger.logger.info(F"UDP Message Proto is {str(request)}")
        return data_bytes


if __name__ == "__main__":
    message1 = UdpMessage.get_udp_message_proto(0.0, 0.0, 12.3, 25.0, 5.0)
