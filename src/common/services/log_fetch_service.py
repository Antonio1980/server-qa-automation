import json
import requests
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
from src.common.services.svc_requests.log_fetch_requests import LogFetchServiceRequest
from src.common.services.svc_requests.request_constants import RESPONSE_TEXT


class LogFetchService(ServiceBase):
    def __init__(self):
        super(LogFetchService, self).__init__()
        self.proxy_url = "api/"
        self.url = self.api_base_url + "log-fetch-service/" + self.proxy_url

    @automation_logger(logger)
    def get_tasks(self):
        uri = self.url + "tasks"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_tasks failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_tasks_by_user_id(self, user_id):
        uri = self.url + "tasks/group/" + str(user_id)
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_roup_tasks_by_id failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_tasks_by_id(self, task_id):
        uri = self.url + "tasks/" + str(task_id) + "/file"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(uri, headers=self.headers_without_token)
            try:
                body = json.loads(_response.text)
            except Exception:
                body = _response.text
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_tasks_by_id failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_task(self, user_id):
        uri = self.url + "tasks/"
        payload = LogFetchServiceRequest().add_task(user_id)
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(uri, data=payload, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} set_tasks failed with error: {e}")
            raise e

    @automation_logger(logger)
    def upload_file_task(self, task_id, text):
        uri = self.url + "upload/" + str(task_id)
        headers_ = {"Content-Type": "application/octet-stream"}
        payload = LogFetchServiceRequest().upload_file(text)
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(uri, data=payload,headers=headers_)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} upload_tasks failed with error: {e}")
            raise e

    @automation_logger(logger)
    def delete_tasks(self, user_id):
        uri = self.url + "tasks/" + str(user_id)
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.delete(uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} delete_tasks failed with error: {e}")
            raise e
