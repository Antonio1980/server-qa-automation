import pytest
from src.base.lib_ import logger
from src.base.entities.api_key import ApiKey
from src.base.lib_.log_decorator import automation_logger


@pytest.fixture
@automation_logger(logger)
def api_key():
    api_key = ApiKey("QA-Test").set_api_key(["QA", "11111", "Test"], 100, 200)
    logger.logger.info(f"API key is: {api_key}")
    return api_key


@pytest.fixture
@automation_logger(logger)
def api_name(request, api_client, api_key):
    name = "server-qa-automation"

    def delete_api():
        res_del = api_client.licensing_svc.delete_client("server-qa-automation")
        assert res_del[1].status_code == 200

    delete_api()

    response_ = api_client.licensing_svc.add_client(name, api_key.__dict__)
    assert response_[1].status_code == 200

    request.addfinalizer(delete_api)

    return response_[0]["clients"]["name"]
