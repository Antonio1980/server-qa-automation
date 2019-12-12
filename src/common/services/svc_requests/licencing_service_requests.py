from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class LicencingServiceRequest(RequestSchema):
    def __init__(self):
        super(LicencingServiceRequest, self).__init__()

    @automation_logger(logger)
    def add_client(self, name: str, api_key: dict):
        self.inner[NAME] = str(name)
        self.inner[API_KEYS] = list()
        self.inner[API_KEYS].append(api_key)
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def validate(self, api_key: str, app_id: str, client_id: str):
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body
