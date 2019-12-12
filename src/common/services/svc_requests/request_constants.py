from src.common.enums import DetectedType

REQUEST_BODY = "Request body: {0}"
RESPONSE_TEXT = "Service Response: {0}"

# Udp requests
ID = "id"
TYPE = "type"
DATA = "data"
CLIENT_DATA = "clientData"
CLIENT_DATA_TYPE = "clientDataType"
LATITUDE = "latitude"
LONGITUDE = "longitude"
BEARING = "bearing"
VELOCITY = "velocity"
HORIZONTAL_ACCURACY = "horizontalAccuracy"
TIMESTAMP = "timestamp"
SOURCE = "source"
DEBUG_MODE = "debugMode"

# Area-Blacklist
SW = "sw"
NE = "ne"
LNG = "lng"
LAT = "lat"
DESCRIPTION = "description"
POSITION = "position"
SHAPE = "shape"
SHAPE_ID = "shape_id"
IS_ACTIVE = "isActive"

# Location
DATA_LIST = "dataList"
ALTITUDE = "altitude"
AVG_ACCELERATION = "avgAcceleration"
AVG_ANGULAR_CHANGE = "avgAngularChange"
BREAKING_STRANGE_PERCENT = "breakingStrengthPercent"
MAX_ACCELERATION = "maxAcceleration"
MAX_ANGULAR_CHANGE = "maxAngularChange"
MAX_DECELERATION = "maxDeceleration"
RAW_HORIZONTAL_ACCURACY = "rawHorizontalAccuracy"
SESSION_ID = "sessionId"
VERTICAL_ACCURACY = "verticalAccuracy"
DEFINITIONS_DELETE = "definitionsToDelete"
DEFINITIONS_UPDATE = "definitionsToUpdate"
DEFINITION_ID = "definitionId"
NICKNAME = "nickname"


# Log-fetch
NOTIFY_SLACK = "notifySlack"
SLACK_NOTIFY_STATUS = "slackNotifyStatus"

# Messages
USER_ID = "userid"
TASKS = "tasks"
TO = "to"
FROM = "from"
TASK_ID = "taskid"
DISTRIBUTION_TYPE = "distributionType"

# Remote-config
HASH = "hash"
SWAGGER = "swagger"
PARAM1 = "param1"
PARAM2 = "param2"
PARAM3 = "param3"

# Reporting
CLIENT_ID = "clientId"
PARAMS = "params"
REPORT_TYPE = "reportType"
GENERAL_INFO = "generalInfo"

# Routing
BUILD_TIME = "buildTime"
BOUNDING_BOX = "boundingBox"
COUNT_BY_TYPE = "countByType"
MAX_LAT = "maxLat"
MAX_LON = "maxLon"
MIN_LAT = "minLat"
MIN_LON = "minLon"
CAR = DetectedType.CAR.value
PEDESTRIAN = DetectedType.PEDESTRIAN.value
BIKE = DetectedType.BIKE.value
IP = "ip"
MIN_PORT = "minPort"
MAX_PORT = "maxPort"
NAME = "name"
PRIORITY = "priority"
INSTANCE_ID = "instanceId"
JVM_LOAD = "jvmLoad"
REGION = "region"
REVISION = "revision"
SYSTEM_LOAD = "systemLoad"
TIME_STARTED = "timeStarted"
PROVIDER = "provider"

# Licencing
API_KEYS = "apiKeys"

