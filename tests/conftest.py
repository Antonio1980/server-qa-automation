import time
import pytest
from src.common import logger
from src.common.log_decorator import automation_logger

collect_ignore = ["setup.py"]


@pytest.fixture(scope="class")
@automation_logger(logger)
def run_time_count(request):
    start_time = time.perf_counter()
    logger.logger.info("START TIME: {0}".format(start_time))

    def stop_counter():
        end_time = time.perf_counter()
        logger.logger.info(F"END TIME: {end_time}")
        average_time = time.strptime(time.ctime(end_time - start_time), "%a %b %d %H:%M:%S %Y")
        min_ = average_time.tm_min
        sec_ = average_time.tm_sec
        logger.logger.info("AVERAGE OF THE TEST CASE RUN TIME: {0} minutes {1} seconds".format(min_, sec_))

    request.addfinalizer(stop_counter)


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
