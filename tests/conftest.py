import os
import time
import pytest
from src.common import logger
from src.common.api_client import ApiClient
from src.common.log_decorator import automation_logger


@pytest.fixture(scope="class")
@automation_logger(logger)
def run_time_counter(request):
    start_time = time.perf_counter()
    logger.logger.info("START TIME: {0}".format(start_time))

    def stop_counter():
        end_time = time.perf_counter()
        logger.logger.info(F"END TIME: {end_time}")
        average_time = time.strptime(time.ctime(end_time - start_time), "%a %b %d %H:%M:%S %Y")
        min_ = average_time.tm_min
        sec_ = average_time.tm_sec
        logger.logger.info("AVERAGE OF THE TEST CASE RUN TIME: {0} minutes {1} seconds".format(min_, sec_))
        time.sleep(1.0)

    request.addfinalizer(stop_counter)


@pytest.fixture(scope="class")
@automation_logger(logger)
def endpoints():
    response_ = ApiClient().routing_svc.get_endpoints()[0]
    return response_


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
    env = os.environ.get('ENV')
    if isinstance(env, str):
        return env
    else:
        os.environ["ENV"] = "stg"
        return "stg"


@pytest.mark.usefixtures("env")
def pytest_report_header(config):
    if config.getoption("verbose") > 0:
        return [f"Environment is {os.environ.get('ENV').upper()}", "Let's test eyenet..."]


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:

            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""

            f.write(rep.nodeid + extra + "\n")


# def pytest_addoption(parser):
#     parser.addoption(
#         "--expect_endpoints", action="store", default="2", help="Please, set an expected endpoints (int).")
#
#
# @pytest.fixture
# def expect_endpoints(request):
#     return request.config.getoption("--expect_endpoints")
#