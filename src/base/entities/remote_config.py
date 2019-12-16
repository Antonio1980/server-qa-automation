from src.base.utils import logger
from src.base.entities.entity import Entity
from src.base.utils.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import SWAGGER, PARAM1, PARAM2, PARAM3
from src.base.utils.utils import Utils


class RemoteConfig(Entity):
    def __init__(self, config_hash=None):
        super(RemoteConfig, self).__init__()
        self.config_hash = config_hash
        self.name = Utils.get_random_string()
        self.description = "QA Test"
        self.data = dict()

    @automation_logger(logger)
    def set_config(self, swagger: bool, *args):
        (param1, param2, param3, ) = args
        self.data[SWAGGER] = swagger
        self.data[PARAM1] = param1
        self.data[PARAM2] = param2
        self.data[PARAM3] = param3
        return self
