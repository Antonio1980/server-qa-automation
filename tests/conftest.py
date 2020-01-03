import os
import time
import pytest
import datetime
from src.base.lib_ import logger
from src.base.enums.enums import Environment
from src.base.instruments.udp_socket import UdpSocket
from src.base.instruments.api_client import ApiClient
from src.base.lib_.log_decorator import automation_logger
from src.base.lib_.auth_zero import AuthorizationZero


@pytest.fixture(scope="session", autouse=True)
def check_environment_marks(pytestconfig, env):
    markers_arg = pytestconfig.getoption('-m')
    if env.lower() == "prod" and markers_arg != "liveness":
        pytest.exit("PRODUCTION env. accepts ONLY LIVENESS tests !!!")


@pytest.fixture(scope="class")
@automation_logger(logger)
def run_time_counter(request):
    time.sleep(1.0)
    start_time = time.perf_counter()
    logger.logger.info("START TIME: {0}".format(start_time))

    def stop_counter():
        end_time = time.perf_counter()
        logger.logger.info("END TIME: {0}".format(end_time))
        average_time = datetime.datetime.strptime(time.ctime(end_time - start_time), "%a %b %d %H:%M:%S %Y")
        min_, sec_, m_sec = average_time.minute, average_time.second, average_time.microsecond
        logger.logger.info(f"AVERAGE OF THE TEST CASE RUN TIME: {min_} minutes {sec_} seconds {m_sec} microseconds")
        time.sleep(1.0)

    request.addfinalizer(stop_counter)


@pytest.fixture(scope="session")
@automation_logger(logger)
def api_client():
    auth_token = AuthorizationZero.get_authorization_token()["access_token"]
    return ApiClient(auth_token)


@pytest.fixture(scope="class")
@automation_logger(logger)
def locations(api_client):
    _response = api_client.routing_svc.get_location_services_v1()
    assert _response[1].status_code == 200
    return _response[0]


@pytest.fixture(scope="class")
@automation_logger(logger)
def new_definition(request, api_client):
    ne_lat, ne_lng = 45.680180, -92.807291
    sw_lat, sw_lng = 37.029238, -113.338244
    definition_id, res = "", dict()

    from src.base.entities.bounding_box import BoundingBox

    usa_box = BoundingBox().set_bounding_box(max_lat=ne_lat, max_lon=ne_lng, min_lat=sw_lat, min_lon=sw_lng)

    _response = api_client.routing_svc.create_location_definitions(usa_box, "GOOGLE", 1, "TEST")
    assert _response[1].status_code == 200

    for item in _response[0]["definitions"]:
        if item["region"] == "TEST":
            definition_id = item["definitionId"]
            res = item

    def clean_definition():
        api_client.routing_svc.delete_location_definitions(definition_id)

    request.addfinalizer(clean_definition)

    return res


@pytest.fixture(scope="class")
@automation_logger(logger)
def socket_(request):
    sock = UdpSocket()
    logger.logger.info(f"UDP Socket ready for connection: {sock.__class__.__name__}")

    def close_socket():
        logger.logger.info("Closing UDP Socket.")
        sock.__exit__()

    request.addfinalizer(close_socket)
    return sock


@pytest.fixture
@automation_logger(logger)
def new_task(request, api_client):
    res = None

    def delete_task():
        del_res = api_client.log_fetch_svc.delete_user_tasks("server-qa-automation")
        assert del_res[1].status_code == 200, "Known Issue # BUG V2X-1878"

    delete_task()

    _response = api_client.log_fetch_svc.add_task("server-qa-automation")
    assert _response[1].status_code == 200

    _response = api_client.log_fetch_svc.get_tasks()[0]

    for item in _response["tasks"]:
        if item["userid"] == "server-qa-automation" and item["status"] == "Pending":
            res = item

    request.addfinalizer(delete_task)

    return res


@pytest.fixture
@automation_logger(logger)
def uploaded_task(new_task, api_client):
    task_id = new_task["taskid"]
    try:
        return api_client.log_fetch_svc.upload_file_task(task_id, "Test QA")[0]
    except Exception as e:
        logger.logger(F"Error on fixture uploaded_task: {e}")
        raise e


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" % previousfailed.name)


@pytest.fixture(scope="class")
@automation_logger(logger)
def stderr_stdout(capsys):
    # or use "capfd" for fd-level
    try:
        captured = capsys.readouterr()
        return captured.out, captured.err
    except Exception as ex:
        logger.logger.exception(F"stderr_stdout failed wih error: {ex}")
        raise ex


@pytest.fixture(scope="session")
def env():
    env_ = os.environ.get('ENV')
    if isinstance(env_, str):
        return env_
    else:
        os.environ["ENV"] = Environment.STAGING.value
        return Environment.STAGING.value


@pytest.mark.usefixtures("env")
def pytest_report_header(config):
    if config.getoption("verbose") > 0:
        return [f"Environment is {os.environ.get('ENV').upper()}", "Let's test eyenet API ..."]


# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#
#     outcome = yield
#     rep = outcome.get_result()
#
#     if rep.when == "call" and rep.failed:
#         mode = "a" if os.path.exists("failures") else "w"
#         with open("failures", mode) as f:
#
#             if "tmpdir" in item.fixturenames:
#                 extra = " (%s)" % item.funcargs["tmpdir"]
#             else:
#                 extra = ""
#
#             f.write(rep.nodeid + extra + "\n")
#
#
# def pytest_addoption(parser):
#     parser.addoption(
#         "--expect_endpoints", action="store", default="2", help="Please, set an expected _endpoints (int).")
#
#
# @pytest.fixture
# def expect_endpoints(request):
#     return request.config.getoption("--expect_endpoints")
