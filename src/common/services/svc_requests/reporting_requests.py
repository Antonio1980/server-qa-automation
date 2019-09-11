import json
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class ReportingServiceRequest(RequestSchema):
    def __init__(self):
        super(ReportingServiceRequest, self).__init__()

    @automation_logger(logger)
    def analytics_report(self, app_client, report_item_list: list):
        body_list = list()
        for item in report_item_list:
            inner = dict()
            inner[CLIENT_ID] = app_client.id
            inner[ID] = item.id
            inner[PARAMS] = dict()
            if item.report_type == "AppStart":
                inner[PARAMS][GENERAL_INFO] = dict()
                inner[PARAMS][GENERAL_INFO].update(app_client.device.__dict__)
            else:
                inner[PARAMS].update(item.params)
            inner[REPORT_TYPE] = item.report_type
            inner[SESSION_ID] = item.session_id
            inner[TIMESTAMP] = item.timestamp
            body_list.append(inner)
        if len(body_list) == 1:
            body = body_list.pop()
            body = json.dumps(body, default=lambda o: vars(o), sort_keys=True, indent=4)
            logger.logger.info(REQUEST_BODY.format(body))
            return body
        else:
            logger.logger.info(REQUEST_BODY.format(body_list))
            return json.dumps(body_list)

    @automation_logger(logger)
    def location_history_report(self, location):
        self.inner[DATA] = list()
        self.inner[DATA].append(dict())
        self.inner[DATA][0][ID] = location.id
        self.inner[DATA][0][ALTITUDE] = location.latitude
        self.inner[DATA][0][AVG_ACCELERATION] = location.avg_acceleration
        self.inner[DATA][0][AVG_ANGULAR_CHANGE] = location.avg_angular_change
        self.inner[DATA][0][BEARING] = location.bearing
        self.inner[DATA][0][BREAKING_STRANGE_PERCENT] = location.breaking_strange_percent
        self.inner[DATA][0][CLIENT_DATA_TYPE] = location.client_data_type
        self.inner[DATA][0][HORIZONTAL_ACCURACY] = location.horizontal_accuracy
        self.inner[DATA][0][LATITUDE] = location.latitude
        self.inner[DATA][0][LONGITUDE] = location.longitude
        self.inner[DATA][0][MAX_ACCELERATION] = location.max_acceleration
        self.inner[DATA][0][MAX_ANGULAR_CHANGE] = location.max_angular_change
        self.inner[DATA][0][MAX_DECELERATION] = location.max_deceleration
        self.inner[DATA][0][RAW_HORIZONTAL_ACCURACY] = location.raw_horizontal_accuracy
        self.inner[DATA][0][SESSION_ID] = location.session_id
        self.inner[DATA][0][SOURCE] = location.source
        self.inner[DATA][0][TIMESTAMP] = location.timestamp
        self.inner[DATA][0][VELOCITY] = location.velocity
        self.inner[DATA][0][VERTICAL_ACCURACY] = location.vertical_accuracy
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body
