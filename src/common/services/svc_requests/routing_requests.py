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
        self.inner[CLIENT_ID] = client_id
        self.inner[ID] = report_item.id
        self.inner[PARAMS] = dict()
        self.inner[PARAMS].update(report_item.params)
        self.inner[REPORT_TYPE] = report_item.report_type
        self.inner[SESSION_ID] = report_item.session_id
        self.inner[TIMESTAMP] = report_item.timestamp
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def keep_alive(self, bounding_box, route, *args):
        ((car, pedestrian, bike, ), ) = args
        self.inner[BOUNDING_BOX] = dict()
        self.inner[BOUNDING_BOX][MAX_LAT] = bounding_box.max_lat
        self.inner[BOUNDING_BOX][MAX_LON] = bounding_box.max_lon
        self.inner[BOUNDING_BOX][MIN_LAT] = bounding_box.min_lat
        self.inner[BOUNDING_BOX][MIN_LON] = bounding_box.min_lon
        self.inner[COUNT_BY_TYPE] = dict()
        self.inner[COUNT_BY_TYPE][CAR] = car
        self.inner[COUNT_BY_TYPE][PEDESTRIAN] = pedestrian
        self.inner[COUNT_BY_TYPE][BIKE] = bike
        body = {**json.loads(self.from_json("inner")), **json.loads(Utils.from_json(route))}
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def add_route(self, location):
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
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body
