import json
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class AreasBlacklistServiceRequest(RequestSchema):
    def __init__(self):
        super(AreasBlacklistServiceRequest, self).__init__()

    @automation_logger(logger)
    def add_areas(self, *args):
        ((ne_lng, ne_lat, sw_lng, sw_lat, ), ) = args
        self.inner[DESCRIPTION] = "description"
        self.inner[POSITION] = dict()
        self.inner[POSITION][SW] = dict()
        self.inner[POSITION][SW][LNG] = sw_lng
        self.inner[POSITION][SW][LAT] = sw_lat
        self.inner[POSITION][NE] = dict()
        self.inner[POSITION][NE][LNG] = ne_lng
        self.inner[POSITION][NE][LAT] = ne_lat
        body = json.dumps(json.loads(self.to_json()).pop("inner"))
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def get_areas_inbox(self, *args):
        ((ne_lng, ne_lat, sw_lng, sw_lat, ), ) = args
        self.inner[SHAPE] = dict()
        self.inner[SHAPE][SW] = dict()
        self.inner[SHAPE][SW][LNG] = sw_lng
        self.inner[SHAPE][SW][LAT] = sw_lat
        self.inner[SHAPE][NE] = dict()
        self.inner[SHAPE][NE][LNG] = ne_lng
        self.inner[SHAPE][NE][LAT] = ne_lat
        body = json.dumps(json.loads(self.to_json()).pop("inner"))
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def activate_area(self, shape_id, status):
        self.inner[SHAPE_ID] = shape_id
        self.inner[IS_ACTIVE] = status
        body = json.dumps(json.loads(self.to_json()).pop("inner"))
        logger.logger.info(REQUEST_BODY.format(body))
        return body
