from src.common.utils.slack import Slack
from src.common.utils.utils import Utils
from src.common.utils.auth_zero import AuthorizationZero


class Instruments(AuthorizationZero, Slack, Utils):
    pass