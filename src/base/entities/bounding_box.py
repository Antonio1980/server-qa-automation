from src.base.lib_ import logger
from src.base.entities.entity import Entity
from src.base.lib_.log_decorator import automation_logger


class BoundingBox(Entity):
    def __init__(self):
        super(BoundingBox, self).__init__()
        self.max_lat = 0.0
        self.max_lon = 0.0
        self.min_lat = 0.0
        self.min_lon = 0.0

    @automation_logger(logger)
    def set_bounding_box(self, max_lat: float, max_lon: float, min_lat: float, min_lon: float):
        self.max_lat = max_lat
        self.max_lon = max_lon
        self.min_lat = min_lat
        self.min_lon = min_lon
        return self
