from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class AreasBlacklistServiceRequest(RequestSchema):
    def __init__(self):
        super(AreasBlacklistServiceRequest, self).__init__()

    @automation_logger(logger)
    def add_areas(self, *args):
        ((ne_lng, ne_lat, sw_lng, sw_lat, ),) = args
        self.description = "description"
        self.position = {}
        self.position[SW] = {}
        self.position[SW][LNG] = sw_lng
        self.position[SW][LAT] = sw_lat
        self.position[NE] = {}
        self.position[NE][LNG] = ne_lng
        self.position[NE][LAT] = ne_lat
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def get_areas_inbox(self, *args):
        ((ne_lng, ne_lat, sw_lng, sw_lat, ),) = args
        self.shape = {}
        self.shape[SW] = {}
        self.shape[SW][LNG] = sw_lng
        self.shape[SW][LAT] = sw_lat
        self.shape[NE] = {}
        self.shape[NE][LNG] = ne_lng
        self.shape[NE][LAT] = ne_lat
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def activate_area(self, shape_id, status):
        self.shape_id = shape_id
        self.isActive = status
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
