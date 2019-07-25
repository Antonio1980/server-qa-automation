from src.common import logger
from src.common.log_decorator import automation_logger


class Route(object):
    def __init__(self, ip="127.0.0.1"):
        super(Route, self).__init__()
        self.ip = ip
        self.name = ""
        self.priority = 0
        self.max_port = None
        self.min_port = None

    @automation_logger(logger)
    def set_route(self, ip: str, name: str, priority: int, port_list: list):
        self.ip = ip
        self.name = str(name)
        self.priority = int(priority)
        self.max_port = port_list[0]
        self.min_port = port_list[1]
        logger.logger.info(F"Route: {self}")
        return self


    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ', '.join("{k}={v}".format(k=k, v=self.__dict__[k])
                                         for k in sorted(self.__dict__.keys())))
