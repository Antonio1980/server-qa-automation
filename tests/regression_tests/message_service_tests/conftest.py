import pytest
from src.base.lib_ import logger
from src.base.lib_.utils import Utils
from src.base.lib_.log_decorator import automation_logger

_task_id = Utils.get_random_string()


@pytest.fixture
@automation_logger(logger)
def new_message(request, api_client):
    del_resp = api_client.message_svc.get_messages()[0]["messagesArray"]
    for m in del_resp:
        if "userid" in m.keys():
            if "server-qa-automation" in m["userid"]:
                del_ = api_client.message_svc.delete_user_messages("server-qa-automation")
                assert del_[1].status_code == 200

    _response = api_client.message_svc.add_messages("server-qa-automation", "sendLog", _task_id)
    assert _response[1].status_code == 200

    response_ = api_client.message_svc.get_messages()[0]
    res = None

    for message in response_["messagesArray"]:
        if "userid" in message.keys():
            if "server-qa-automation" in message["userid"]:
                logger.logger.info(f"Test message is found- {message}")
                res = message

    def delete_message():
        resp = api_client.message_svc.delete_user_messages("server-qa-automation")
        assert resp[1].status_code == 200

    request.addfinalizer(delete_message)

    return res
