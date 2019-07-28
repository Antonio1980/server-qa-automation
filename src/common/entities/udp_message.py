import random
from src.common import logger
from src.common.entities.entity import Entity
from src.common.instruments import Instruments
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *


class UdpMessage(Entity):
    def __init__(self, debug_mode=True):
        super(UdpMessage, self).__init__()
        self.type = "LocationUpdate2"
        self.data = dict()
        self.data[DEBUG_MODE] = debug_mode

    @automation_logger(logger)
    def set_udp_message(self, *args):
        """

        :param args: latitude- str, longitude- str, bearing- int (0-1), velocity- int (0-1), accuracy- float
        """
        (latitude, longitude, bearing, velocity, accuracy) = args
        self.data[CLIENT_DATA] = dict()
        timestamp_ = Instruments.get_synch_timestamp()
        while timestamp_ is None:
            timestamp_ = Instruments.get_synch_timestamp()
        self.data[CLIENT_DATA][TIMESTAMP] = timestamp_
        self.data[CLIENT_DATA][ID] = "QA_test_" + str(random.randint(0, 1000))
        self.data[CLIENT_DATA][CLIENT_DATA_TYPE] = "CAR"
        self.data[CLIENT_DATA][LATITUDE] = str(latitude)
        self.data[CLIENT_DATA][LONGTITUDE] = str(longitude)
        self.data[CLIENT_DATA][BEARING] = bearing
        self.data[CLIENT_DATA][VELOCITY] = velocity
        self.data[CLIENT_DATA][HORIZONTAL_ACCURACY] = float(accuracy)
        self.data[CLIENT_DATA][SOURCE] = "QA Test"
        logger.logger.info(F"UDP Message is {self.to_json()}")
        return self

    @automation_logger(logger)
    def get_udp_message(self, *args):
        (latitude, longitude, bearing, velocity, accuracy) = args
        return Instruments.from_json(self.set_udp_message(latitude, longitude, bearing, velocity, accuracy)).encode("utf8")
