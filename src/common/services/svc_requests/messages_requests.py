from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class MessagesServiceRequest(RequestSchema):
    def __init__(self):
        super(MessagesServiceRequest, self).__init__()

    @automation_logger(logger)
    def set_messages(self, user_id, message_type, task_id):
        self.inner[TYPE] = message_type
        self.inner[USER_ID] = user_id
        self.inner[DATA] = dict()
        self.inner[DATA][TASKS].extend([
            {
                TO: self.timestamp_to,
                FROM: self.timestamp_from,
                TASK_ID: task_id
            }
        ])
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body
