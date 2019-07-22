from socket import *
from src.common import logger
from src.common.log_decorator import automation_logger


class UdpSocket(object):
    def __init__(self):
        super(UdpSocket, self).__init__()
        self.udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
        self.udp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.udp_socket.setsockopt(SOL_SOCKET, MSG_WAITALL, 1)
        self.udp_socket.settimeout(2)

    @automation_logger(logger)
    def udp_connect(self, address):
        logger.logger.info('UDP client is Up!')
        self.udp_socket.connect(address)

    @automation_logger(logger)
    def udp_send(self, bytes_to_send: bytes):
        self.udp_socket.send(bytes_to_send)
        logger.logger.info('UDP message is sent!')

    @automation_logger(logger)
    def udp_send_to(self, bytes_to_send: bytes, address: tuple):
        self.udp_socket.sendto(bytes_to_send, address)
        logger.logger.info(F'UDP message is sent to {address}')

    @automation_logger(logger)
    def udp_receive(self, buf_size):
        _response = self.udp_socket.recv(buf_size).decode()
        logger.logger.info(F"UDP response is: {_response}")
        return _response
