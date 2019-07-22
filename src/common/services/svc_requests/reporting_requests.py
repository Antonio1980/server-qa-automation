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
