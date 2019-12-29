import pytest
from threading import Thread
from src.base.utils import logger
from src.base.utils.log_decorator import automation_logger

user_id = "server-qa-automation"
num_threads = 50
num_loops = 20


@pytest.fixture(autouse=True)
@automation_logger(logger)
def _1000_user_messages(request, api_client):

    def del_messages():
        api_client.log_fetch_svc.delete_user_tasks(user_id)

    del_messages()

    def _messages():
        temp = []
        for _ in range(num_loops):
            resp = api_client.log_fetch_svc.add_task(user_id)
            assert resp[1].status_code == 200
            temp.append(resp[1].status_code)
        assert len(temp) == 20

    for i in range(num_threads):
        worker = Thread(target=_messages)
        worker.setDaemon(True)
        worker.start()
        worker.join(1.0)

    request.addfinalizer(del_messages)
