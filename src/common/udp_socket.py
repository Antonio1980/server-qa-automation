import random
from socket import *
from src.common import logger
from src.common.utils.utils import Utils
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class UdpSocket:
    udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
    udp_socket.settimeout(1.0)

    @classmethod
    @automation_logger(logger)
    def udp_send(cls, bytes_to_send: bytes, address: tuple):
        logger.logger.info("UDP client up and listening")
        cls.udp_socket.sendto(bytes_to_send, address)


class UdpMessage(RequestSchema):
    def __init__(self, debug_mode=True):
        super(UdpMessage, self).__init__()
        self.type = "LocationUpdate2"
        self.data = dict()
        self.data[DEBUG_MODE] = debug_mode

    @automation_logger(logger)
    def udp_message(self, *args):
        """

        :param args: latitude- str, longitude- str, bearing- int (0-1), velocity- int (0-1), accuracy- float
        """
        (latitude, longitude, bearing, velocity, accuracy) = args

        self.data[CLIENT_DATA] = dict()
        self.data[CLIENT_DATA][ID] = "QA_test_" + str(random.randint(0, 100))
        self.data[CLIENT_DATA][CLIENT_DATA_TYPE] = "CAR"
        self.data[CLIENT_DATA][LATITUDE] = str(latitude)
        self.data[CLIENT_DATA][LONGTITUDE] = str(longitude)
        self.data[CLIENT_DATA][BEARING] = bearing
        self.data[CLIENT_DATA][VELOCITY] = velocity
        self.data[CLIENT_DATA][HORIZONTAL_ACCURACY] = float(accuracy)
        self.data[CLIENT_DATA][TIMESTAMP] = self.timestamp
        self.data[CLIENT_DATA][SOURCE] = "QA Test"

        body = Utils.to_json(self)
        logger.logger.info(REQUEST_BODY.format(body))
        return body
