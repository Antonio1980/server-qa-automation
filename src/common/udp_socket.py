from socket import *
from src.common import logger
from src.common.log_decorator import automation_logger


class UdpSocket:
    udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
    udp_socket.settimeout(1)

    @classmethod
    @automation_logger(logger)
    def udp_send(cls, bytes_to_send: bytes, address: tuple):
        logger.logger.info("UDP client is Up!")
        cls.udp_socket.sendto(bytes_to_send, address)
