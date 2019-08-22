from socket import *
from src.common import logger
from src.common.log_decorator import automation_logger


class UdpSocket(object):
    def __init__(self):
        super(UdpSocket, self).__init__()
        self.udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
        self.udp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.udp_socket.setsockopt(SOL_SOCKET, MSG_WAITALL, 1)
        self.udp_socket.settimeout(1)

    @automation_logger(logger)
    def udp_connect(self, address):
        try:
            self.udp_socket.connect(address)
            logger.logger.info('UDP client is Up!')
        except Exception as e:
            logger.logger.error(F"udp_connect failed with error: {e.with_traceback(e.__traceback__)}")

    @automation_logger(logger)
    def udp_send(self, bytes_to_send: bytes):
        try:
            self.udp_socket.send(bytes_to_send)
            logger.logger.info('UDP message is sent!')
        except Exception as e:
            logger.logger.error(F"udp_send failed with error: {e.with_traceback(e.__traceback__)}")

    @automation_logger(logger)
    def udp_send_to(self, bytes_to_send: bytes, address: tuple):
        try:
            self.udp_socket.sendto(bytes_to_send, address)
            logger.logger.info(F'UDP message is sent to {address}')
        except Exception as e:
            logger.logger.error(F"udp_send_to failed with error: {e.with_traceback(e.__traceback__)}")

    @automation_logger(logger)
    def udp_receive(self, buf_size):
        try:
            while True:
                _response = self.udp_socket.recv(buf_size)
                if len(_response) <= 0:
                    break
                logger.logger.info(F"UDP response is: {_response}")
                return _response
        except TimeoutError as e:
            logger.logger.error(F"udp_receive failed with error: {e.with_traceback(e.__traceback__)}")
