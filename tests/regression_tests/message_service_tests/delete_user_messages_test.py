import allure
import pytest
from src.base.instruments.api_client import ApiClient
from src.base.utils import logger
from config_definitions import BaseConfig
from src.base.utils.log_decorator import automation_logger

test_case = "DELETE MESSAGE"


@allure.title(test_case)
@allure.description("""
    Functional test.
    1. Check that service is responded on "DeletetMessage" request properly.
    2. Check that service response contains desired properties.
    3. Negative: Check that without authorization it forbidden.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "regression_tests/message_service_tests/delete_user_messages_test.py",
                 "TestDeleteUserMessages")
@pytest.mark.regression
@pytest.mark.regression_message
class TestDeleteUserMessages:

    @pytest.fixture
    @automation_logger(logger)
    def _message(self, api_client):
        _response = api_client.message_svc.add_messages("server-qa-automation", "sendLog", "_task_id")
        assert _response[1].status_code == 200

        response_ = api_client.message_svc.get_messages()[0]
        for message in response_["messagesArray"]:
            if "userid" in message.keys():
                if "server-qa-automation" in message["userid"]:
                    logger.logger.info(f"Test message is found- {message}")
                    return message

    @automation_logger(logger)
    def test_delete_user_messages_method_works(self, api_client, _message):
        allure.step("Verify that response is not empty and status code is 200")
        _response = api_client.message_svc.delete_user_messages(_message["userid"])

        assert _response[1].status_code == 200
        assert _response[0] is not None

        logger.logger.info(F"============ TEST CASE {test_case} / 1 PASSED ===========")

    @automation_logger(logger)
    def test_attributes_in_delete_user_messages_method(self, api_client, _message):
        allure.step("Verify response properties and that 'messages' is list object.")
        _response = api_client.message_svc.delete_user_messages(_message["userid"])[0]

        assert isinstance(_response, dict)
        assert "delete" in _response.keys()
        assert "_id" and "type" and "userid" and "data" and "distributionType" in _response["delete"].keys()
        assert _response["delete"]["type"] == _message["type"]
        assert _response["delete"]["userid"] == _message["userid"]
        assert isinstance(_response["delete"]["data"], dict)
        assert "tasks" in _response["delete"]["data"].keys()
        assert isinstance(_response["delete"]["data"]["tasks"], list)
        assert len(_response["delete"]["data"]["tasks"]) > 0

        logger.logger.info(F"============ TEST CASE {test_case} / 2 PASSED ===========")

    @automation_logger(logger)
    def test_delete_user_messages_negative(self, new_message):
        allure.step("Verify that without authorization status code is 401")
        api_ = ApiClient()
        _response = api_.message_svc.delete_user_messages(new_message["userid"])

        assert isinstance(_response[0], dict)
        assert "name" and "message" and "code" and "status" and "inner" in _response[0].keys()
        assert _response[0]['code'] == "credentials_required"
        assert _response[0]['message'] == "No authorization token was found"
        assert _response[1].status_code == 401, "Known Issue # BUG  V2X-1890"

        logger.logger.info(F"============ TEST CASE {test_case} / 3 PASSED ===========")
