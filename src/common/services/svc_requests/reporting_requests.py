from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class ReportingServiceRequest(RequestSchema):
    def __init__(self):
        super(ReportingServiceRequest, self).__init__()

    @automation_logger(logger)
    def analytics_report(self, client_id, report_item):
        self.clientId = client_id
        self.id = report_item.id
        self.params = {}
        self.params.update(report_item.params)
        self.reportType = report_item.report_type
        self.sessionId = report_item.session_id
        self.timestamp = report_item.timestamp
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def location_history_report(self, location):
        self.data = list()
        self.data[0] = {}
        self.data[0][ID] = location.id
        self.data[0][ALTITUDE] = location.latitude
        self.data[0][AVG_ACCELERATION] = location.avg_acceleration
        self.data[0][AVG_ANGULAR_CHANGE] = location.avg_angular_change
        self.data[0][BEARING] = location.bearing
        self.data[0][BREAKING_STRANGE_PERCENT] = location.breaking_strange_percent
        self.data[0][CLIENT_DATA_TYPE] = location.client_data_type
        self.data[0][HORIZONTAL_ACCURACY] = location.horizontal_accuracy
        self.data[0][LATITUDE] = location.latitude
        self.data[0][LONGTITUDE] = location.longitude
        self.data[0][MAX_ACCELERATION] = location.max_acceleration
        self.data[0][MAX_ANGULAR_CHANGE] = location.max_angular_change
        self.data[0][MAX_DECELERATION] = location.max_deceleration
        self.data[0][RAW_HORIZONTAL_ACCURACY] = location.raw_horizontal_accuracy
        self.data[0][SESSION_ID] = location.session_id
        self.data[0][SOURCE] = location.source
        self.data[0][TIMESTAMP] = location.timestamp
        self.data[0][VELOCITY] = location.velocity
        self.data[0][VERTICAL_ACCURACY] = location.vertical_accuracy
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
