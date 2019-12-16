import json

from src.base.utils import logger
from src.base.utils.log_decorator import automation_logger


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
        self.min_port = port_list[0]
        self.max_port = port_list[1]
        return self

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda obj: vars(obj), sort_keys=True, indent=4))
