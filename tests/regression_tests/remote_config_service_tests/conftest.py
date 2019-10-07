import pytest
from src.common import logger
from src.common.utils.utils import Utils
from src.common.api_client import ApiClient
from src.common.entities.remote_config import RemoteConfig
from src.common.log_decorator import automation_logger


@pytest.fixture
@automation_logger(logger)
def get_config_default_name():
    _response = ApiClient().remote_config_svc.get_default_config()[0]
    return _response["name"]


@pytest.fixture
@automation_logger(logger)
def config_hash(get_config_default_name):
    _response = ApiClient().remote_config_svc.get_remote_config_hash(get_config_default_name)[0]
    return _response["hash"]["hash"]


@pytest.fixture
@automation_logger(logger)
def remote_config(config_hash):
    remote_config = RemoteConfig(config_hash).set_config(False, True, 12345, "abc")
    return remote_config


@pytest.fixture
@automation_logger(logger)
def add_new_config():
    remote_config = RemoteConfig(Utils.get_timestamp).set_config(False, True, 12345, "qa")
    _response = ApiClient().remote_config_svc.add_remote_config(remote_config)
    return _response
