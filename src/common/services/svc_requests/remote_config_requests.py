from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class RemoteConfigServiceRequest(RequestSchema):
    def __init__(self):
        super(RemoteConfigServiceRequest, self).__init__()
        self.hash = ""
        self.data = {}

    @automation_logger(logger)
    def set_config(self, hash, data):
        self.hash = hash
        self.data.update(data)
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
