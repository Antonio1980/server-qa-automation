from src.common.utils.slack import Slack
from src.common.utils.utils import Utils
from src.common.data_bases.kibana import KibanaCli
from src.common.data_bases.mongo_cli import MongoCli
from src.common.utils.auth_zero import AuthorizationZero


class Instruments(AuthorizationZero, Slack, Utils, MongoCli, KibanaCli):
    def __init__(self):
        super(Instruments, self).__init__(AuthorizationZero.__init__(self))
        pass
