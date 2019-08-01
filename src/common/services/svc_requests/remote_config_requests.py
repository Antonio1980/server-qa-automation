from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class RemoteConfigServiceRequest(RequestSchema):
    def __init__(self):
        super(RemoteConfigServiceRequest, self).__init__()

    @automation_logger(logger)
    def add_config(self, remote_config):
        self.inner[HASH] = remote_config.config_hash
        self.inner[DATA] = dict()
        self.inner[DATA].update(remote_config.data)
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body
