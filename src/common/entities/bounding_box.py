from src.common.entities.entity import Entity


class BoundingBox(Entity):
    def __init__(self):
        super(BoundingBox, self).__init__()
        self.max_lat = 0
        self.max_lon = 0
        self.min_lat = 0
        self.min_lon = 0

    def set_bounding_box(self, ne_lat: float, ne_lon: float, sw_lat: float, sw_lon: float):
        self.max_lat = ne_lat
        self.max_lon = ne_lon
        self.min_lat = sw_lat
        self.min_lon = sw_lon
        return self
