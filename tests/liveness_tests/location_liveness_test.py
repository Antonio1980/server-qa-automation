import random
import allure
import pytest
from src.base.utils import logger
from src.base.utils.slack import Slack
from config_definitions import BaseConfig
from src.base.entities.udp_message import UdpMessage
from src.base.utils.log_decorator import automation_logger
from src.base.automation_error import AutomationError

test_case = "LIVENESS LOCATION"
BUFSIZ = 1024


@allure.feature("LIVENESS")
@allure.story('Client able to found and connect to Location service via min and max ports.')
@allure.title(test_case)
@allure.description("""
    Functional end to end test.
    1. Check that number of Location definition returned in response "get state" equals to number of instances.
    2. Check (for every instance) that Location service allows connections by provided min/max ports.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "liveness_tests/location_liveness_test.py", "TestLiveness")
@pytest.mark.liveness
class TestLiveness(object):
    issues = ""
    latitude = "0.0"
    longitude = "0.0"
    bearing = random.uniform(0, 360)
    velocity = random.uniform(2, 40)
    accuracy = 5.0

    @automation_logger(logger)
    def test_returned_locations(self, locations):
        allure.step("Verify that Routing svc sum of returned location definitions equals to sum returned instances. ")

        definitions_len, instances_len = len(locations["definitions"]), len(locations["instances"])
        if_err_message = f"Definitions count {definitions_len} != number of instances {instances_len}"

        if definitions_len != instances_len:
            TestLiveness.issues += if_err_message
            logger.logger.exception(if_err_message)

            raise AutomationError(if_err_message)
        else:
            logger.logger.info(F"Routing svc returned {definitions_len} endpoints -> PASSED !")

    @automation_logger(logger)
    def test_endpoints_ports(self, locations, socket_):
        allure.step("Verify that all provided ports are open and accept UDP connections.")

        for instance in locations["instances"]:
            port_range = [instance["minPort"], instance["maxPort"]]

            for port in port_range:
                socket_.udp_connect((instance["ip"], port))

                if_error = F"The instance {instance['instanceId']} is not responding on port {port} ! \n"
                message1 = UdpMessage().get_udp_message(self.latitude, self.longitude, self.bearing,
                                                        self.velocity, self.accuracy)
                message2 = UdpMessage().get_udp_message(self.latitude, self.longitude, self.bearing,
                                                        self.velocity, self.accuracy)
                try:
                    socket_.udp_send(message1)

                    socket_.udp_send(message2)
                    response_ = socket_.udp_receive(BUFSIZ)
                except Exception as ex:
                    response_ = None
                    if_data_error = F"Error occurred while receiving data: {ex} \n"
                    logger.logger.exception(if_data_error)
                    TestLiveness.issues += if_data_error
                if response_:
                    logger.logger.info(F"The instance {instance['instanceId']} available for connect on port {port} !")
                    logger.logger.info(F"UDP Response: {response_}")
                else:
                    TestLiveness.issues += if_error
                    logger.logger.error(f"{if_error}")

        if TestLiveness.issues:
            logger.logger.fatal(f"{TestLiveness.issues}")
            Slack.send_message(TestLiveness.issues)

            raise AutomationError(F"============ TEST CASE {test_case} FAILED ===========")
        else:
            logger.logger.info(F"============ TEST CASE {test_case} PASSED ===========")
