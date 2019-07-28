from src.common import logger
from src.common.log_decorator import automation_logger


class BoundingBox(object):
    def __init__(self):
        super(BoundingBox, self).__init__()
        self.max_lat = 0
        self.max_lon = 0
        self.min_lat = 0
        self.min_lon = 0

    @automation_logger(logger)
    def set_bounding_box(self, max_lat: float, max_lon: float, min_lat: float, min_lon: float):
        self.max_lat = max_lat
        self.max_lon = max_lon
        self.min_lat = min_lat
        self.min_lon = min_lon
        logger.logger.info(F"BoundingBox: {self}")
        return self

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ', '.join("{k}={v}".format(k=k, v=self.__dict__[k])
                                         for k in sorted(self.__dict__.keys())))
