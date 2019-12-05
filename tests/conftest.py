import datetime
import os
import time
import pytest
from src.common import logger
from src.common.enums import Environment
from src.common.api_client import ApiClient
from src.common.instruments import Instruments
from src.common.udp_socket import UdpSocket
from src.common.log_decorator import automation_logger


@pytest.fixture(scope="session", autouse=True)
def check_environment_marks(pytestconfig, env):
    markers_arg = pytestconfig.getoption('-m')
    if env.lower() == "prod" and markers_arg != "liveness":
        pytest.exit("PRODUCTION env. accepts ONLY LIVENESS tests !!!")


@pytest.fixture(scope="class")
@automation_logger(logger)
def run_time_counter(request):
    start_time = time.perf_counter()
    logger.logger.info("START TIME: {0}".format(start_time))

    def stop_counter():
        end_time = time.perf_counter()
        logger.logger.info("END TIME: {0}".format(end_time))
        average_time = datetime.datetime.strptime(time.ctime(end_time - start_time), "%a %b %d %H:%M:%S %Y")
        min_ = average_time.minute
        sec_ = average_time.second
        m_sec = average_time.microsecond
        logger.logger.info(f"AVERAGE OF THE TEST CASE RUN TIME: {min_} minutes {sec_} seconds {m_sec} microseconds")
        time.sleep(1.0)

    request.addfinalizer(stop_counter)


@pytest.fixture(scope="session")
@automation_logger(logger)
def api_client():
    auth_token = Instruments.get_authorization_token()["access_token"]
    return ApiClient(auth_token)


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


@pytest.fixture(scope="class")
@automation_logger(logger)
def endpoints(api_client):
    _response = api_client.routing_svc.get_endpoints()[0]
    return _response


@pytest.fixture
@automation_logger(logger)
def add_task(api_client):
    api_client.log_fetch_svc.add_task("qa_test_qa")


@pytest.fixture
@automation_logger(logger)
def get_task(add_task, api_client):
    logger.logger.info(f"Task is added- {add_task}")
    _response = api_client.log_fetch_svc.get_tasks()[0]

    for item in _response["tasks"]:
        if (item["userid"] == "qa_test_qa" or item["userid"] == "another_qa_test_qa") and item["status"] == "Pending":
            return item


@pytest.fixture
@automation_logger(logger)
def get_uploaded_task(get_task, api_client):
    task_id = get_task["taskid"]
    try:
        return api_client.log_fetch_svc.upload_file_task(task_id, "Test QA")[0]
    except Exception as e:
        logger.logger(F"Error on fixture get_uploaded_task: {e}")
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
    except Exception as e:
        logger.logger.exception(F"stderr_stdout failed wih error: {e}")
        raise e


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
