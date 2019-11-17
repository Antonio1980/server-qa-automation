import pytest
from src.common import logger
from src.common.utils.utils import Utils
from src.common.entities.remote_config import RemoteConfig
from src.common.log_decorator import automation_logger


@pytest.fixture
@automation_logger(logger)
def get_config_default_name(api_client):
    _response = api_client.remote_config_svc.get_default_config()[0]
    return _response["name"]


@pytest.fixture
@automation_logger(logger)
def config_hash(get_config_default_name, api_client):
    _response = api_client.remote_config_svc.get_remote_config_hash(get_config_default_name)[0]
    return _response["hash"]["hash"]


@pytest.fixture
@automation_logger(logger)
def remote_config(request, api_client):
    remote_config = RemoteConfig(Utils.get_timestamp()).set_config(False, True, 12345, Utils.get_random_string(6))
    logger.logger.info(remote_config.__repr__())

    def del_config():
        res = api_client.remote_config_svc.delete_remote_config(remote_config.name)
        assert res[1].status_code == 200

    request.addfinalizer(del_config)

    return remote_config


@pytest.fixture
@automation_logger(logger)
def new_remote_config(api_client):
    remote_config = RemoteConfig(Utils.get_timestamp()).set_config(False, True, 12345, Utils.get_random_string(6))
    _response = api_client.remote_config_svc.add_remote_config(remote_config)
    return _response[0]["name"]
