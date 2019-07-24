import json
import requests
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
from src.common.services.svc_requests.messages_requests import MessagesServiceRequest
from src.common.services.svc_requests.request_constants import RESPONSE_TEXT


class MessagesService(ServiceBase):
    def __init__(self):
        super(MessagesService, self).__init__()
        self.proxy_url = "api/"
        self.url = self.api_base_url + "messages-service/" + self.proxy_url

    @automation_logger(logger)
    def get_messages(self):
        uri = self.url + "messages/"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_messages failed with error: {e}")
            raise e

    @automation_logger(logger)
    def set_messages(self):
        uri = self.url + "messages/"
        payload = MessagesServiceRequest().set_messages()
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(uri, data=payload, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} set_messages failed with error: {e}")
            raise e

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

    @automation_logger(logger)
    def delete_user_messages(self, user_id):
        uri = self.url + "messages/" + str(user_id)
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.delete(uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} delete_user_messages failed with error: {e}")
            raise e
