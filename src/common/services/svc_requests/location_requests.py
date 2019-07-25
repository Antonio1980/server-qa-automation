import json
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class LocationServiceRequest(RequestSchema):
    def __init__(self):
        super(LocationServiceRequest, self).__init__()

    @automation_logger(logger)
    def add_locations(self, location):
        self.inner[ID] = location.id
        self.inner[ALTITUDE] = location.altitude
        self.inner[AVG_ACCELERATION] = location.avg_acceleration
        self.inner[AVG_ANGULAR_CHANGE] = location.avg_angular_change
        self.inner[BEARING] = location.bearing
        self.inner[BREAKING_STRANGE_PERCENT] = location.breaking_strange_percent
        self.inner[CLIENT_DATA_TYPE] = location.client_data_type
        self.inner[HORIZONTAL_ACCURACY] = location.horizontal_accuracy
        self.inner[LATITUDE] = location.latitude
        self.inner[LONGTITUDE] = location.longitude
        self.inner[MAX_ACCELERATION] = location.max_acceleration
        self.inner[MAX_ANGULAR_CHANGE] = location.max_angular_change
        self.inner[MAX_DECELERATION] = location.max_deceleration
        self.inner[RAW_HORIZONTAL_ACCURACY] = location.raw_horizontal_accuracy
        self.inner[SESSION_ID] = location.session_id
        self.inner[SOURCE] = location.source
        self.inner[TIMESTAMP] = location.timestamp
        self.inner[VELOCITY] = location.velocity
        self.inner[VERTICAL_ACCURACY] = location.vertical_accuracy
        body = json.dumps(json.loads(self.to_json()).pop("inner"))
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def add_multiple_locations(self, location):
        self.inner[DATA_LIST] = list()
        self.inner[DATA_LIST].extend([
            {
                ID: location.id,
                ALTITUDE: location.altitude,
                AVG_ACCELERATION: location.avg_acceleration,
                AVG_ANGULAR_CHANGE: location.avg_angular_change,
                BEARING: location.bearing,
                BREAKING_STRANGE_PERCENT: location.breaking_strange_percent,
                CLIENT_DATA_TYPE: location.client_data_type,
                HORIZONTAL_ACCURACY: location.horizontal_accuracy,
                LATITUDE: location.latitude,
                LONGTITUDE: location.longitude,
                MAX_ACCELERATION: location.max_acceleration,
                MAX_ANGULAR_CHANGE: location.max_angular_change,
                MAX_DECELERATION: location.max_deceleration,
                RAW_HORIZONTAL_ACCURACY: location.raw_horizontal_accuracy,
                SESSION_ID: location.session_id,
                SOURCE: location.source,
                TIMESTAMP: location.timestamp,
                VELOCITY: location.velocity,
                VERTICAL_ACCURACY: location.vertical_accuracy
            }
        ])
        body = json.dumps(json.loads(self.to_json()).pop("inner"))
        logger.logger.info(REQUEST_BODY.format(body))
        return body


# if __name__ == "__main__":
#     from src.common.entities.location import Location
#     import json
#     l = Location()
#     r = LocationServiceRequest().add_locations(l)
#     pass