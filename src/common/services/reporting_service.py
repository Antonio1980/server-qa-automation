import requests
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
from src.common.services.svc_requests.reporting_requests import ReportingServiceRequest
from src.common.services.svc_requests.request_constants import *


class ReportingService(ServiceBase):
    def __init__(self):
        super(ReportingService, self).__init__()
        self.url = self.api_base_url + "reporting-service/v1/"

    @automation_logger(logger)
    def analytics(self, client_id, report_item):
        uri = self.url + "analytics"
        try:
            payload = ReportingServiceRequest().analytics(client_id, report_item)
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers_without_token)
            body = "OK"
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} analytics failed with error: {e}")
            raise e