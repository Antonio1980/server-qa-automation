import pytest
from src.base.utils import logger
from src.base.entities.api_key import ApiKey
from src.base.utils.log_decorator import automation_logger
from src.base.utils.utils import Utils


@pytest.fixture
@automation_logger(logger)
def api_key():
    api_key = ApiKey("QA-Test").set_api_key(["QA", "11111", "Test"], 100, 200)
    logger.logger.info(f"API key is: {api_key}")
    return api_key


@pytest.fixture
@automation_logger(logger)
def api_name(api_client, api_key):
    name = Utils.get_random_string(size=6)
    _response = api_client.licensing_svc.add_client(name, api_key.__dict__)
    assert _response[0] is not None
    assert _response[1].status_code == 200
    return name