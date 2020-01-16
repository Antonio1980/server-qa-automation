import pytest
from threading import Thread

user_id = "server-qa-automation"
num_threads = 20
num_loops = 50


@pytest.fixture
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
        return

    for i in range(num_threads):
        worker = Thread(target=_messages, daemon=True)
        worker.start()
        worker.join()

    request.addfinalizer(del_messages)
