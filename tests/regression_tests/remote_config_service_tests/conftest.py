import pytest
from src.base.utils import logger
from src.base.utils.utils import Utils
from src.base.entities.remote_config import RemoteConfig
from src.base.utils.log_decorator import automation_logger


@pytest.fixture
@automation_logger(logger)
def get_config_default_name(api_client):
    _response = api_client.remote_config_svc.get_default_config()[0]
    return _response["name"]


@pytest.fixture
@automation_logger(logger)
def config_default_hash(get_config_default_name, api_client):
    _response = api_client.remote_config_svc.get_remote_config_hash(get_config_default_name)[0]
    return _response["hash"]["hash"]


@pytest.fixture
@automation_logger(logger)
def remote_config():
    remote_config_ = RemoteConfig(Utils.get_timestamp()).set_config(False, True, 12345, "QA-Test")
    logger.logger.info(remote_config_.__repr__())

    return remote_config_


@pytest.fixture
@automation_logger(logger)
def new_remote_config(request, api_client, remote_config):

    def delete_config():
        conf_resp = api_client.remote_config_svc.get_configs()
        assert conf_resp[1].status_code == 200

        for item in conf_resp[0]:
            if item["name"] is not None:
                if item["name"] == "server-qa-automation":
                    del_res = api_client.remote_config_svc.delete_remote_config(item["name"])
                    assert del_res[1].status_code == 200

    delete_config()

    _response = api_client.remote_config_svc.add_remote_config(remote_config)
    assert _response[1].status_code == 200
    assert isinstance(_response[0], dict)

    request.addfinalizer(delete_config)

    return _response[0]
