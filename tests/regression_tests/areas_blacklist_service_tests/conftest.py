import pytest
from src.common import logger
from src.common.utils.utils import Utils
from src.common.api_client import ApiClient
from src.common.entities.bounding_box import BoundingBox
from src.common.log_decorator import automation_logger


ne_lat, ne_lng = 0.0, 0.0
sw_lat, sw_lng = 0.0, 0.0
empty_box = BoundingBox().set_bounding_box(ne_lat, ne_lng, sw_lat, sw_lng)


@pytest.fixture
@automation_logger(logger)
def add_area():
    _response = ApiClient().areas_blacklist_svc.add_areas("qa_test_qa" + Utils.get_random_string(), empty_box)[1]
    assert _response.status_code == 201


@pytest.fixture
@automation_logger(logger)
def get_area(add_area):
    _response = ApiClient().areas_blacklist_svc.get_areas()[0]

    for area in _response["areas"]:
        if "qa_test_qa" in area["description"] and area["isActive"] is True:
            logger.logger.info(f"Test area is found- {area}")
            return area
