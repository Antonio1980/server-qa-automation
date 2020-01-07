import pytest
from src.base.lib_.log_decorator import automation_logger
from src.base.lib_.logger import logger
from src.proto import LocationServiceRequest_pb2
from src.proto import LocationServiceResponse_pb2
from src.proto import ClientLocationData_pb2
from src.proto import ClientData_pb2


@pytest.mark.skip
@pytest.mark.protobuf
class TestCheckAllPortsWithProtobuf(object):

    @automation_logger(logger)
    def test_protobuf(self):
        request = LocationServiceRequest_pb2.LocationServiceRequest()
        # response = LocationServiceResponse_pb2.LocationServiceResponse()
        request.type = LocationServiceRequest_pb2.LocationServiceRequest.MessageType.CLIENT_LOCATION
        # request.clientLocationData = ClientLocationData_pb2.ClientLocationData()
        request.clientLocationData.debugMode = True
        request.clientLocationData.notifyMe = True
        request.clientLocationData.notifyOthers = True
        request.clientLocationData.clientData.id = "server-qa-automation"
        request.clientLocationData.clientData.latitude = 31.1
        request.clientLocationData.clientData.longitude = 32.2
        request.clientLocationData.clientData.clientDataType = ClientData_pb2.ClientData.LocationBearerType.CAR
        binaryMessage = request.SerializeToString()
        readableMessage = str(request)
        logger.logger.info(f"A: {readableMessage}")
        # logger.logger.info(F"B: {request.__dict__}")
        logger.logger.info(f"C: {request}")
        # response = LocationServiceResponse_pb2.LocationServiceResponse()
        # response.ParseFromString("tergfr")
