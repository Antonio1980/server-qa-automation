import random
from src.base.utils import logger
from src.base.entities.entity import Entity
from src.base.utils.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.utils.utils import Utils


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
        self.data[CLIENT_DATA][ID] = "QA_test_" + str(random.randint(0, 1000))
        self.data[CLIENT_DATA][CLIENT_DATA_TYPE] = DetectedType.CAR.value
        self.data[CLIENT_DATA][LATITUDE] = str(latitude)
        self.data[CLIENT_DATA][LONGITUDE] = str(longitude)
        self.data[CLIENT_DATA][BEARING] = bearing
        self.data[CLIENT_DATA][VELOCITY] = velocity
        self.data[CLIENT_DATA][HORIZONTAL_ACCURACY] = float(accuracy)
        self.data[CLIENT_DATA][SOURCE] = "QA Test"
        logger.logger.info(F"UDP Message is {self.to_json()}")
        return Utils.to_json_dumps(self).encode("utf8")
