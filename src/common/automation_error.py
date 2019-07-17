from src.common import logger
from src.common.log_decorator import automation_logger


class AutomationError(Exception):
    
    def __init__(self, *args):
        super(Exception, self).__init__(*args)

    @automation_logger(logger)
    def __str__(self):
        return "Automation error is occurred: {0}".format(self.args)

    @automation_logger(logger)
    def __repr__(self):
        return "Automation error is occurred: {0}".format(self.__str__())
