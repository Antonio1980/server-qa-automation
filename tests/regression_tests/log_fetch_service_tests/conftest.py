import pytest
from threading import Thread

user_id = "server-qa-automation"
num_threads = 10
num_loops = 100


@pytest.fixture(scope="class")
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
        assert len(temp) == num_loops

    for i in range(num_threads):
        worker = Thread(target=_messages, daemon=True)
        worker.setDaemon(True)
        worker.start()
        worker.join(1.0)

    request.addfinalizer(del_messages)
