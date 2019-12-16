from src.common.utils import logger
from src.common.utils.utils import Utils
from src.common.utils.log_decorator import automation_logger
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.request_schema import RequestSchema


class RoutingServiceRequest(RequestSchema):
    def __init__(self):
        super(RoutingServiceRequest, self).__init__()

    @automation_logger(logger)
    def analytics(self, client_id, report_item):
        self.inner[CLIENT_ID] = client_id
        self.inner[ID] = report_item.id
        self.inner[PARAMS] = dict()
        self.inner[PARAMS].update(report_item.params)
        self.inner[REPORT_TYPE] = report_item.report_type
        self.inner[SESSION_ID] = report_item.session_id
        self.inner[TIMESTAMP] = report_item.timestamp
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def update_definitions(self, box, *args):
        if args and len(args[0]) > 0:
            ((id_, priority, region,),) = args
        else:
            id_, priority, region = None, None, None
        self.inner[DEFINITIONS_DELETE] = list()
        self.inner[DEFINITIONS_UPDATE] = list()
        self.inner[DEFINITIONS_UPDATE].append(dict())
        self.inner[DEFINITIONS_UPDATE][0][BOUNDING_BOX] = dict()
        self.inner[DEFINITIONS_UPDATE][0][BOUNDING_BOX][MAX_LAT] = box.max_lat
        self.inner[DEFINITIONS_UPDATE][0][BOUNDING_BOX][MAX_LON] = box.max_lon
        self.inner[DEFINITIONS_UPDATE][0][BOUNDING_BOX][MIN_LAT] = box.min_lat
        self.inner[DEFINITIONS_UPDATE][0][BOUNDING_BOX][MIN_LON] = box.min_lat
        self.inner[DEFINITIONS_UPDATE][0][DEFINITION_ID] = id_
        self.inner[DEFINITIONS_UPDATE][0][DESCRIPTION] = "QA Test"
        self.inner[DEFINITIONS_UPDATE][0][NICKNAME] = Utils.get_random_string(size=6)
        self.inner[DEFINITIONS_UPDATE][0][PRIORITY] = priority
        self.inner[DEFINITIONS_UPDATE][0][REGION] = region
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def keep_alive(self, route, *args):
        if args and len(args[0]) > 0:
            ((car, pedestrian, bike, ), ) = args
        else:
            car, pedestrian, bike = 0, 0, 0

        self.inner[BUILD_TIME] = Utils.get_random_string()
        self.inner[COUNT_BY_TYPE] = dict()
        self.inner[COUNT_BY_TYPE][CAR] = car
        self.inner[COUNT_BY_TYPE][PEDESTRIAN] = pedestrian
        self.inner[COUNT_BY_TYPE][BIKE] = bike
        self.inner[INSTANCE_ID] = Utils.get_random_string()
        self.inner[IP] = route.ip
        self.inner[JVM_LOAD] = 0
        self.inner[PROVIDER] = route.name
        self.inner[MIN_PORT] = route.min_port
        self.inner[MAX_PORT] = route.max_port
        self.inner[REGION] = "QA"
        self.inner[REVISION] = "Test"
        self.inner[SYSTEM_LOAD] = 0
        self.inner[TIME_STARTED] = Utils.get_timestamp()
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def add_route(self, location):
        self.inner[ID] = location.id
        self.inner[ALTITUDE] = location.altitude
        self.inner[AVG_ACCELERATION] = location.avg_acceleration
        self.inner[AVG_ANGULAR_CHANGE] = location.avg_angular_change
        self.inner[BEARING] = location.bearing
        self.inner[BREAKING_STRANGE_PERCENT] = location.breaking_strange_percent
        self.inner[CLIENT_DATA_TYPE] = location.client_data_type
        self.inner[HORIZONTAL_ACCURACY] = location.horizontal_accuracy
        self.inner[LATITUDE] = location.latitude
        self.inner[LONGITUDE] = location.longitude
        self.inner[MAX_ACCELERATION] = location.max_acceleration
        self.inner[MAX_ANGULAR_CHANGE] = location.max_angular_change
        self.inner[MAX_DECELERATION] = location.max_deceleration
        self.inner[SESSION_ID] = location.session_id
        self.inner[SOURCE] = location.source
        self.inner[TIMESTAMP] = location.timestamp
        self.inner[VELOCITY] = location.velocity
        self.inner[VERTICAL_ACCURACY] = location.vertical_accuracy
        body = self.from_json("inner")
        logger.logger.info(REQUEST_BODY.format(body))
        return body
