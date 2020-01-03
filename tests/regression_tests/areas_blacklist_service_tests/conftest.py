import pytest
from src.base.lib_ import logger
from src.base.entities.bounding_box import BoundingBox
from src.base.lib_.log_decorator import automation_logger


ne_lat, ne_lng = 0.0, 0.0
sw_lat, sw_lng = 0.0, 0.0
empty_box = BoundingBox().set_bounding_box(ne_lat, ne_lng, sw_lat, sw_lng)


@pytest.fixture
@automation_logger(logger)
def new_area(request, api_client):
    del_resp = api_client.areas_blacklist_svc.get_areas()[0]["areas"]
    for i in del_resp:
        if i["description"] == "server-qa-automation":
            d_resp = api_client.areas_blacklist_svc.delete_areas_by_id(i["_id"])
            assert d_resp[1].status_code == 200

    _response = api_client.areas_blacklist_svc.add_areas("server-qa-automation", empty_box)[1]
    assert _response.status_code == 201

    _response = api_client.areas_blacklist_svc.get_areas()[0]
    res, shape_id = None, None

    for area in _response["areas"]:
        if "server-qa-automation" in area["description"] and area["isActive"] is True:
            logger.logger.info(f"Test area is found- {area}")
            shape_id = area["_id"]
            res = area

    def delete_area():
        resp = api_client.areas_blacklist_svc.delete_areas_by_id(shape_id=shape_id)
        assert resp[1].status_code == 200

    request.addfinalizer(delete_area)

    return res
