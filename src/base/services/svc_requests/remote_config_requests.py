from src.base.utils import logger
from src.base.utils.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import RequestSchema


class RemoteConfigServiceRequest(RequestSchema):
    def __init__(self):
        super(RemoteConfigServiceRequest, self).__init__()

    @automation_logger(logger)
    def add_config(self, remote_config):
        self.inner[HASH] = remote_config.config_hash
        self.inner[NAME] = remote_config.name
        self.inner[DESCRIPTION] = remote_config.description
        self.inner[DATA] = dict()
        self.inner[DATA].update(remote_config.data)
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body
