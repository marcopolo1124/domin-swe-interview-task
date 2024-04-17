import socket
import logging
from multiprocessing import Queue
import msvcrt
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
SOCKET_ADDR = ("localhost", 12346)



def udp_listener(q: Queue):
    logger.log(logging.INFO, "start listening")
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(SOCKET_ADDR)
    while True:
        (msg, _) = client.recvfrom(1024)
        q.put(msg.decode())