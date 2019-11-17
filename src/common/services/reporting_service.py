import json
import requests
from src.common import logger
from json import JSONDecodeError
from src.common.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
from src.common.services.svc_requests.request_constants import RESPONSE_TEXT
from src.common.services.svc_requests.reporting_requests import ReportingServiceRequest


class ReportingService(ServiceBase):
    def __init__(self, auth_token):
        super(ReportingService, self).__init__()
        if auth_token:
            self.headers.update({'Authorization': 'Bearer {0}'.format(auth_token)})
        self.version = "v1/"
        self.url = self.api_base_url + "reporting-service/"

    @automation_logger(logger)
    def add_analytics_report(self, app_client, report_item):
        uri = self.url + self.version + "analytics"
        try:
            payload = ReportingServiceRequest().analytics_report(app_client, [report_item])
            logger.logger.info(F"API Service URL is POST- {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers_without_token)
            body = _response.reason
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} analytics failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_bulk_analytics_report(self, app_client: str, report_item_list: list) -> tuple:
        uri = self.url + self.version + "analytics/bulk"
        try:
            payload = ReportingServiceRequest().analytics_report(app_client, report_item_list)
            logger.logger.info(F"API Service URL is POST- {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers)
            if _response.status_code == 401:
                body = json.loads(_response.text)
            else:
                body = _response.reason
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} bulk_analytics_report failed with error: {e}")
            raise e

    @automation_logger(logger)
    def old_analytics_report(self, client_id, report_item):
        uri = self.url + self.version + "analytics/old"
        try:
            payload = ReportingServiceRequest().analytics_report(client_id, report_item)
            logger.logger.info(F"API Service URL is POST- {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers_without_token)
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
            logger.logger.error(F"{e.__class__.__name__} old_analytics_report failed with error: {e}")
            raise e

    @automation_logger(logger)
    def location_history_report(self, location):
        uri = self.url + self.version + "location-history"
        try:
            payload = ReportingServiceRequest().location_history_report(location)
            logger.logger.info(F"API Service URL is POST- {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers)
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
            logger.logger.error(F"{e.__class__.__name__} location_history_report failed with error: {e}")
            raise e

    @automation_logger(logger)
    def binary_location_history_report(self):
        uri = self.url + self.version + "location-history/binary"
        try:
            logger.logger.info(F"API Service URL is POST- {uri}")
            _response = requests.post(url=uri, headers=self.headers_without_token)
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
            logger.logger.error(F"{e.__class__.__name__} binary_location_history_report failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_version_info(self):
        uri = self.url + "version-info"
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
            logger.logger.error(F"{e.__class__.__name__} get_version_info failed with error: {e}")
            raise e

    @automation_logger(logger)
    def health(self):
        uri = self.url + "actuator/health"
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
