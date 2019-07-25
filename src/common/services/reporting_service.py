import json
import requests
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
from src.common.services.svc_requests.request_constants import RESPONSE_TEXT
from src.common.services.svc_requests.reporting_requests import ReportingServiceRequest


class ReportingService(ServiceBase):
    def __init__(self):
        super(ReportingService, self).__init__()
        self.proxy_url = "v1/"
        self.url = self.api_base_url + "reporting-service/" + self.proxy_url

    @automation_logger(logger)
    def analytics_report(self, client_id, report_item):
        uri = self.url + "analytics"
        try:
            payload = ReportingServiceRequest().analytics_report(client_id, report_item)
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers_without_token)
            body = "OK"
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} analytics failed with error: {e}")
            raise e

    @automation_logger(logger)
    def bulk_analytics_report(self, client_id, report_item):
        uri = self.url + "analytics/bulk"
        try:
            payload = ReportingServiceRequest().analytics_report(client_id, report_item)
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers_without_token)
            body = "OK"
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} bulk_analytics_report failed with error: {e}")
            raise e

    @automation_logger(logger)
    def old_analytics_report(self, client_id, report_item):
        uri = self.url + "analytics/old"
        try:
            payload = ReportingServiceRequest().analytics_report(client_id, report_item)
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers_without_token)
            body = "OK"
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} old_analytics_report failed with error: {e}")
            raise e

    @automation_logger(logger)
    def location_history_report(self, location):
        uri = self.url + "location-history"
        try:
            payload = ReportingServiceRequest().location_history_report(location)
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers_without_token)
            body = "OK"
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} location_history_report failed with error: {e}")
            raise e

    @automation_logger(logger)
    def binary_location_history_report(self, location):
        uri = self.url + "location-history/binary"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(url=uri, headers=self.headers_without_token)
            body = "OK"
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} binary_location_history_report failed with error: {e}")
            raise e

    @automation_logger(logger)
    def binary_location_history_report(self, location):
        uri = self.url + "extension/binary"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(url=uri, headers=self.headers_without_token)
            body = "OK"
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} binary_location_history_report failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_version_info(self):
        uri = self.url + "version-info"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_version_info failed with error: {e}")
            raise e
