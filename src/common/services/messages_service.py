import json
import requests
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
from src.common.services.svc_requests.request_constants import *


class MessagesService(ServiceBase):
    def __init__(self):
        super(MessagesService, self).__init__()
        self.url = self.api_base_url + "messages-service/api/"

    @automation_logger(logger)
    def get_user_messages(self, user_id):
        uri = self.url + "messages/user/" + str(user_id)
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_user_messages failed with error: {e}")
            raise e
