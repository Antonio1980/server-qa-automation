from src.base.lib_ import logger
from src.base.lib_.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import RequestSchema


class MessagesServiceRequest(RequestSchema):
    def __init__(self):
        super(MessagesServiceRequest, self).__init__()

    @automation_logger(logger)
    def add_messages(self, user_id, message_type, task_id):
        self.inner[TYPE] = message_type
        self.inner[USER_ID] = user_id
        self.inner[DISTRIBUTION_TYPE] = "SpecificUser"
        self.inner[DATA] = dict()
        self.inner[DATA][TASKS] = list()
        self.inner[DATA][TASKS].extend([
            {
                TO: self.curr_date,
                FROM: self.past_date,
                TASK_ID: task_id
            }
        ])
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body
