from src.common.utils.utils import Utils


class Location(object):
    def __init__(self):
        super(Location, self).__init__()
        self.id = Utils.random_string_generator()
        self.altitude = 0
        self.avg_acceleration = 0
        self.avg_angular_change = 0
        self.bearing = 0
        self.breaking_strange_percent = 0
        self.client_data_type = ""
        self.horizontal_accuracy = 0
        self.latitude = 0
        self.longitude = 0
        self.max_acceleration = 0
        self.max_angular_change = 0
        self.max_deceleration = 0
        self.raw_horizontal_accuracy = 0
        self.session_id = ""
        self.source = ""
        self.timestamp = Utils.get_timestamp()
        self.velocity = 0
        self.vertical_accuracy = 0

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ', '.join("{k}={v}".format(k=k, v=self.__dict__[k])
                                         for k in sorted(self.__dict__.keys())))
