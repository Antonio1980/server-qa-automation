from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class LogFetchServiceRequest(RequestSchema):
    def __init__(self):
        super(LogFetchServiceRequest, self).__init__()

    @automation_logger(logger)
    def add_task(self, user_id):
        self.inner[USER_ID] = user_id
        self.inner[TO] = self.future_date
        self.inner[FROM] = self.curr_date
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
            ################ end ########################
            ################ end ########################
            ################ end ########################
            ################ end ########################
            ################ end ########################
        """
        logger.logger.info(REQUEST_BODY.format(body))
        return body
