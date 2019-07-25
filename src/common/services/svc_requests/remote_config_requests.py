import json
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class RemoteConfigServiceRequest(RequestSchema):
    def __init__(self):
        super(RemoteConfigServiceRequest, self).__init__()

    @automation_logger(logger)
    def set_config(self, hash, data):
        self.inner[HASH] = hash
        self.inner[DATA] = dict()
        self.inner[DATA].update(data)
        body = json.dumps(json.loads(self.to_json()).pop("inner"))
        logger.logger.info(REQUEST_BODY.format(body))
        return body
