from src.common.utils import logger
from src.common.utils.log_decorator import automation_logger


class ApiKey:
    def __init__(self, key: str):
        super(ApiKey, self).__init__()
        self.applicationIds = list()
        self.key = key
        self.quotaWarning = 0
        self.quotaError = 0

    @automation_logger(logger)
    def set_api_key(self, app_ids: list, q_warning: int, q_error: int):
        self.applicationIds.extend(app_ids)
        self.quotaWarning = q_warning
        self.quotaError = q_error
        return self
