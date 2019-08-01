import pytest
from src.common import logger
from src.common.api_client import ApiClient
from src.common.entities.remote_config import RemoteConfig
from src.common.log_decorator import automation_logger


@pytest.fixture
@automation_logger(logger)
def config_hash():
    response_ = ApiClient().remote_config_svc.get_config_hash()[0]
    return response_["currentHash"]


@pytest.fixture
@automation_logger(logger)
def remote_config(config_hash):
    remote_config = RemoteConfig(config_hash).set_config(False, True, 12345, "abc")
    return remote_config
