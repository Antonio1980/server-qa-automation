import json
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class ReportingServiceRequest(RequestSchema):
    def __init__(self):
        super(ReportingServiceRequest, self).__init__()

    @automation_logger(logger)
    def analytics_report(self, client_id, report_item):
        self.inner[CLIENT_ID] = client_id
        self.inner[ID] = report_item.id
        self.inner[PARAMS] = dict()
        self.inner[PARAMS].update(report_item.params)
        self.inner[REPORT_TYPE] = report_item.report_type
        self.inner[SESSION_ID] = report_item.session_id
        self.inner[TIMESTAMP] = report_item.timestamp
        body = json.dumps(json.loads(self.to_json()).pop("inner"))
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def location_history_report(self, location):
        self.inner[DATA] = list()
        self.inner[DATA][0] = dict()
        self.inner[DATA][0][ID] = location.id
        self.inner[DATA][0][ALTITUDE] = location.latitude
        self.inner[DATA][0][AVG_ACCELERATION] = location.avg_acceleration
        self.inner[DATA][0][AVG_ANGULAR_CHANGE] = location.avg_angular_change
        self.inner[DATA][0][BEARING] = location.bearing
        self.inner[DATA][0][BREAKING_STRANGE_PERCENT] = location.breaking_strange_percent
        self.inner[DATA][0][CLIENT_DATA_TYPE] = location.client_data_type
        self.inner[DATA][0][HORIZONTAL_ACCURACY] = location.horizontal_accuracy
        self.inner[DATA][0][LATITUDE] = location.latitude
        self.inner[DATA][0][LONGTITUDE] = location.longitude
        self.inner[DATA][0][MAX_ACCELERATION] = location.max_acceleration
        self.inner[DATA][0][MAX_ANGULAR_CHANGE] = location.max_angular_change
        self.inner[DATA][0][MAX_DECELERATION] = location.max_deceleration
        self.inner[DATA][0][RAW_HORIZONTAL_ACCURACY] = location.raw_horizontal_accuracy
        self.inner[DATA][0][SESSION_ID] = location.session_id
        self.inner[DATA][0][SOURCE] = location.source
        self.inner[DATA][0][TIMESTAMP] = location.timestamp
        self.inner[DATA][0][VELOCITY] = location.velocity
        self.inner[DATA][0][VERTICAL_ACCURACY] = location.vertical_accuracy
        body = json.dumps(json.loads(self.to_json()).pop("inner"))
        logger.logger.info(REQUEST_BODY.format(body))
        return body
