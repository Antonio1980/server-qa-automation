import json
import requests
from src.common.utils import logger
from json import JSONDecodeError
from src.common.utils.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
from src.common.services.svc_requests.request_constants import RESPONSE_TEXT


class MessagesSyncService(ServiceBase):
    def __init__(self, auth_token):
        super(MessagesSyncService, self).__init__()
        if auth_token:
            self.headers.update({'Authorization': 'Bearer {0}'.format(auth_token)})
        self.proxy_url = "api/"
        self.url = self.api_base_url + "messages-sync-service/" + self.proxy_url

    @automation_logger(logger)
    def get_sync_run(self):
        uri = self.url + "sync/run"
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
            logger.logger.error(F"{e.__class__.__name__} get_sync_run failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_sync_access(self):
        uri = self.url + "sync/access"
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
            logger.logger.error(F"{e.__class__.__name__} get_sync_access failed with error: {e}")
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
