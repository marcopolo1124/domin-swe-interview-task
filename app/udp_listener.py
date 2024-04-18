import socket
import socketio
import threading
import logging
from multiprocessing import Queue

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
SOCKET_ADDR = ("localhost", 12346)


def udp_listener(q1: Queue, q2: Queue):
    logger.log(logging.INFO, "start listening")
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(SOCKET_ADDR)
    while True:
        (msg, _) = client.recvfrom(1024)
        decoded = msg.decode()
        q1.put(decoded)
        q2.put(decoded)
        


        