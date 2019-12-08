from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class LogFetchServiceRequest(RequestSchema):
    def __init__(self):
        super(LogFetchServiceRequest, self).__init__()

    @automation_logger(logger)
    def add_task(self, user_id, description, notify_slack):
        self.inner[USER_ID] = user_id
        self.inner[FROM] = self.curr_date
        self.inner[TO] = self.future_date
        self.inner[DESCRIPTION] = description
        self.inner[NOTIFY_SLACK] = notify_slack
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def notify_slack(self, task_id, notify_slack):
        self.inner[TASK_ID] = task_id
        self.inner[SLACK_NOTIFY_STATUS] = notify_slack
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def upload_file(self, text):
        body = F"""
            ################ start ######################
            ################ start ######################
            ################ start ######################
            ################ start ######################
            ################ start ######################
                            {text}
            ################# end ########################
            ################# end ########################
            ################# end ########################
            ################# end ########################
            ################# end ########################
        """
        logger.logger.info(REQUEST_BODY.format(body))
        return body
