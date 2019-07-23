from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class LocationServiceRequest(RequestSchema):
    def __init__(self):
        super(LocationServiceRequest, self).__init__()

    @automation_logger(logger)
    def add_locations(self, location):
        self.id = location.id
        self.altitude = location.altitude
        self.avgAcceleration = location.avg_acceleration
        self.avgAngularChange = location.avg_angular_change
        self.bearing = location.bearing
        self.breakingStrengthPercent = location.breaking_strange_percent
        self.clientDataType = location.client_data_type
        self.horizontalAccuracy = location.horizontal_accuracy
        self.latitude = location.latitude
        self.longitude = location.longitude
        self.maxAcceleration = location.max_acceleration
        self.maxAngularChange = location.max_angular_change
        self.maxDeceleration = location.max_deceleration
        self.rawHorizontalAccuracy = location.raw_horizontal_accuracy
        self.sessionId = location.session_id
        self.source = location.source
        self.timestamp = location.timestamp
        self.velocity = location.velocity
        self.verticalAccuracy = location.vertical_accuracy
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def add_multiple_locations(self, location):
        self.dataList = list()
        self.dataList.extend([
            {
                ID: location.id,
                ATTITUDE: location.altitude,
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
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
