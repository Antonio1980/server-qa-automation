from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class MessagesServiceRequest(RequestSchema):
    def __init__(self):
        super(MessagesServiceRequest, self).__init__()
        self.type = None
        self.userid = None
        self.data = dict()
        self.data[TASKS] = list()

    @automation_logger(logger)
    def set_messages(self, user_id, message_type, task_id):
        self.type = message_type
        self.userid = user_id
        self.data[TASKS].extend([
            {
                TO: self.timestamp_to,
                FROM: self.timestamp_from,
                TASK_ID: task_id
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
