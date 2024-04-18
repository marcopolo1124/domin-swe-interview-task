import csv
import socket
import time
import logging
from threading import Thread

run_listener = True

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
ADDR = ('localhost', 12346)

data = []
with open('sample_vehicle_data_6kph.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a TCP socket
sock.bind(ADDR)
sock.settimeout(0.5)
clients = []

sock.listen(2)
def accept_clients():
    while run_listener:
        try:
            c, addr = sock.accept()
            print("accepted client")
            clients.append((c, addr))
        except socket.timeout:
            pass
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
listen_to_clients = Thread(target=accept_clients)
listen_to_clients.start()                                                                                                                                                   

start_time = time.time()
data = data[2:] # revove the header

logger.log(logging.INFO, 'sending data')

for row in data:
    while (float(row[10]) > time.time() - start_time):
        logger.log(logging.INFO, {'waiting for':row[10]})
        pass
    message = ','.join(row).encode()
    for (client_socket, addr) in clients:
        client_socket.send(message)
    logger.log(logging.DEBUG, {'sent:': message})


logger.log(logging.INFO, 'done')
run_listener = False
listen_to_clients.join()
