from src.base.enums.enums import DetectedType
from src.base.utils.utils import Utils
from src.base.entities.entity import Entity


class Location(Entity):
    def __init__(self, client_type=DetectedType.PEDESTRIAN.value):
        super(Location, self).__init__()
        self.id = Utils.get_random_string()
        self.altitude = 0.0
        self.avg_acceleration = 0
        self.avg_angular_change = 0
        self.bearing = 0
        self.breaking_strange_percent = 0
        self.client_data_type = client_type
        self.horizontal_accuracy = 0
        self.latitude = 0.0
        self.longitude = 0.0
        self.max_acceleration = 0
        self.max_angular_change = 0
        self.max_deceleration = 0
        self.session_id = ""
        self.source = ""
        self.timestamp = self.curr_timestamp
        self.velocity = 0
        self.vertical_accuracy = 0
        self.raw_horizontal_accuracy = 0
