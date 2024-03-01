import csv
import socket
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

data = []
with open('sample_vehicle_data_6kph.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # create a UDP socket

start_time = time.time()
data = data[2:] # revove the header

logger.log(logging.INFO, 'sending data')

for row in data:
    while (float(row[10]) > time.time() - start_time): # check row ts is not in the future
        logger.log(logging.INFO, {'waiting for':row[10]})
        pass
    message = ','.join(row).encode()
    sock.sendto(message, ('localhost', 12345))
    logger.log(logging.INFO, {'sent:': message})

sock.close()
logger.log(logging.INFO, 'done')
