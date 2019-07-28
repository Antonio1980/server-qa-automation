from src.common.entities.entity import Entity


class Route(Entity):
    def __init__(self, ip="127.0.0.1"):
        super(Route, self).__init__()
        self.ip = ip
        self.name = ""
        self.priority = 0
        self.max_port = None
        self.min_port = None

    def set_route(self, ip: str, name: str, priority: int, port_list: list):
        self.ip = ip
        self.name = str(name)
        self.priority = int(priority)
        self.max_port = port_list[0]
        self.min_port = port_list[1]
        return self
