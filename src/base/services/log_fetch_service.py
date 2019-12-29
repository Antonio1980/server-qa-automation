import json
import requests
from src.base.utils import logger
from json import JSONDecodeError
from src.base.utils.log_decorator import automation_logger
from src.base.services.service_base import ServiceBase
from src.base.services.svc_requests.log_fetch_requests import LogFetchServiceRequest
from src.base.services.svc_requests.request_constants import RESPONSE_TEXT


class LogFetchService(ServiceBase):
    def __init__(self, auth_token):
        super(LogFetchService, self).__init__()
        if auth_token:
            self.headers.update({'Authorization': 'Bearer {0}'.format(auth_token)})
        self.proxy_url = "api/"
        self.url = self.api_base_url + "log-fetch-service/" + self.proxy_url

    @automation_logger(logger)
    def get_tasks(self):
        uri = self.url + "tasks"
        try:
            logger.logger.info(F"API Service URL is GET- {uri}")
            _response = requests.get(uri, headers=self.headers)
            try:
                body = json.loads(_response.text)
            except JSONDecodeError as e:
                logger.logger.error(f"Failed to parse response json: {e}")
                if _response.text is not None:
                    body = _response.text
                else:
                    body = _response.reason
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_tasks failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_tasks_grouped_by_user_id(self):
        uri = self.url + "tasks/group/userId"
        try:
            logger.logger.info(F"API Service URL is GET- {uri}")
            _response = requests.get(uri, headers=self.headers)
            try:
                body = json.loads(_response.text)
            except JSONDecodeError as e:
                logger.logger.error(f"Failed to parse response json: {e}")
                if _response.text is not None:
                    body = _response.text
                else:
                    body = _response.reason
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_tasks_grouped_by_user_id failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_file_by_task_id(self, task_id):
        uri = self.url + "tasks/" + str(task_id) + "/file"
        try:
            logger.logger.info(F"API Service URL is GET- {uri}")
            _response = requests.get(uri, headers=self.headers)

            body = _response.text

            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_file_by_task_id failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_task(self, user_id, description="QA-Test", notify_slack=False):
        uri = self.url + "tasks/"
        payload = LogFetchServiceRequest().add_task(user_id, description, notify_slack)
        try:
            logger.logger.info(F"API Service URL is POST- {uri}")
            _response = requests.post(uri, data=payload, headers=self.headers)
            try:
                body = json.loads(_response.text)
            except JSONDecodeError as e:
                logger.logger.error(f"Failed to parse response json: {e}")
                if _response.text is not None:
                    body = _response.text
                else:
                    body = _response.reason
            # logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} add_task failed with error: {e}")
            raise e

    @automation_logger(logger)
    def notify_slack(self, task_id, notify_slack=True):
        uri = self.url + "tasks/notify"
        payload = LogFetchServiceRequest().notify_slack(task_id, notify_slack)
        try:
            logger.logger.info(F"API Service URL is POST- {uri}")
            _response = requests.post(uri, data=payload, headers=self.headers)
            try:
                body = json.loads(_response.text)
            except JSONDecodeError as e:
                logger.logger.error(f"Failed to parse response json: {e}")
                if _response.text is not None:
                    body = _response.text
                else:
                    body = _response.reason
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} notify_slack failed with error: {e}")
            raise e

    @automation_logger(logger)
    def upload_file_task(self, task_id, text):
        uri = self.url + "upload/" + str(task_id)
        _headers = {"Content-Type": "application/octet-stream"}
        payload = LogFetchServiceRequest().upload_file(text)
        try:
            logger.logger.info(F"API Service URL is POST- {uri}")
            _response = requests.post(uri, data=payload, headers=_headers)
            try:
                body = json.loads(_response.text)
            except JSONDecodeError as e:
                logger.logger.error(f"Failed to parse response json: {e}")
                if _response.text is not None:
                    body = _response.text
                else:
                    body = _response.reason
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} upload_file_task failed with error: {e}")
            raise e

    @automation_logger(logger)
    def delete_user_tasks(self, user_id):
        uri = self.url + "tasks/" + str(user_id)
        try:
            logger.logger.info(F"API Service URL is DELETE- {uri}")
            _response = requests.delete(uri, headers=self.headers)
            try:
                body = json.loads(_response.text)
            except JSONDecodeError as e:
                logger.logger.error(f"Failed to parse response json: {e}")
                if _response.text is not None:
                    body = _response.text
                else:
                    body = _response.reason
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} delete_user_tasks failed with error: {e}")
            raise e

    @automation_logger(logger)
    def delete_by_task_id(self, task_id):
        uri = self.url + "tasks/task/" + str(task_id)
        try:
            logger.logger.info(F"API Service URL is DELETE- {uri}")
            _response = requests.delete(uri, headers=self.headers)
            try:
                body = json.loads(_response.text)
            except JSONDecodeError as e:
                logger.logger.error(f"Failed to parse response json: {e}")
                if _response.text is not None:
                    body = _response.text
                else:
                    body = _response.reason
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} delete_by_task_id failed with error: {e}")
            raise e

    @automation_logger(logger)
    def health(self):
        uri = self.url + "health"
        try:
            logger.logger.info(F"API Service URL is GET- {uri}")
            _response = requests.get(uri, headers=self.headers_without_token)
            try:
                body = json.loads(_response.text)
            except JSONDecodeError as e:
                logger.logger.error(f"Failed to parse response json: {e}")
                if _response.text is not None:
                    body = _response.text
                else:
                    body = _response.reason
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} health failed with error: {e}")
            raise e
