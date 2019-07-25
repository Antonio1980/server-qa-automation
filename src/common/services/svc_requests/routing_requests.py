import json
from src.common import logger
from src.common.utils.utils import Utils
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class RoutingServiceRequest(RequestSchema):
    def __init__(self):
        super(RoutingServiceRequest, self).__init__()

    @automation_logger(logger)
    def analytics(self, client_id, report_item):
        self.clientId = client_id
        self.id = report_item.id
        self.params = dict()
        self.params.update(report_item.params)
        self.reportType = report_item.report_type
        self.sessionId = report_item.session_id
        self.timestamp = report_item.timestamp
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def keep_alive(self, bounding_box, route, *args):
        ((car, pedestrian, bike, ), ) = args
        self.boundingBox = dict()
        self.boundingBox[MAX_LAT] = bounding_box.max_lat
        self.boundingBox[MAX_LON] = bounding_box.max_lon
        self.boundingBox[MIN_LAT] = bounding_box.min_lat
        self.boundingBox[MIN_LON] = bounding_box.min_lon
        self.countByType = dict()
        self.countByType[CAR] = car
        self.countByType[PEDESTRIAN] = pedestrian
        self.countByType[BIKE] = bike
        body = {**json.loads(self.to_json()), **json.loads(Utils.to_json(route))}
        body = Utils.to_json(body)
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def add_route(self, location):
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
