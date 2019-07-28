from src.common.utils.slack import Slack
from src.common.utils.utils import Utils
from src.common.utils.ntp_client import NtpClient
from src.common.utils.auth_zero import AuthorizationZero


class Instruments(AuthorizationZero, NtpClient, Slack, Utils):
    pass