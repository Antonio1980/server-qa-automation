from src.base.utils import logger
from src.base.utils.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import RequestSchema


class AreasBlacklistServiceRequest(RequestSchema):
    def __init__(self):
        super(AreasBlacklistServiceRequest, self).__init__()

    @automation_logger(logger)
    def add_areas(self, description, bounding_box):
        self.inner[DESCRIPTION] = str(description)
        self.inner[POSITION] = dict()
        self.inner[POSITION][SW] = dict()
        self.inner[POSITION][SW][LNG] = bounding_box.min_lon
        self.inner[POSITION][SW][LAT] = bounding_box.min_lat
        self.inner[POSITION][NE] = dict()
        self.inner[POSITION][NE][LNG] = bounding_box.max_lon
        self.inner[POSITION][NE][LAT] = bounding_box.max_lat
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def get_areas_inbox(self, bounding_box):
        self.inner[SHAPE] = dict()
        self.inner[SHAPE][SW] = dict()
        self.inner[SHAPE][SW][LNG] = bounding_box.min_lon
        self.inner[SHAPE][SW][LAT] = bounding_box.min_lat
        self.inner[SHAPE][NE] = dict()
        self.inner[SHAPE][NE][LNG] = bounding_box.max_lon
        self.inner[SHAPE][NE][LAT] = bounding_box.max_lat
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def activate_area(self, shape_id, status):
        self.inner[SHAPE_ID] = shape_id
        self.inner[IS_ACTIVE] = status
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body
