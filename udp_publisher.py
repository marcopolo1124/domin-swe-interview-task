'''
this code loads the csv file and the publishees the data on a UDP port.
this is intended to be used for mocking data from a real-time data source.
'''

'''
example data:
altitude,body_x_axis,body_y_axis,body_z_axis,fix,horizontal_dilution,latitude,longitude,num_sats,spd_over_grnd,timestamps,vehicle_accel_x,vehicle_accel_y,vehicle_accel_z,vehicle_gyro_x,vehicle_gyro_y,vehicle_gyro_z,vehicle_mag_x,vehicle_mag_y,vehicle_mag_z,vehicle_orientation_x,vehicle_orientation_y,vehicle_orientation_z,wheel_x_axis,wheel_y_axis,wheel_z_axis
m,g,g,g,bool,count,deg,deg,count,km/h,s,m/s^2,m/s^2,m/s^2,deg/s,deg/s,deg/s,uT,uT,uT,deg,deg,deg,g,g,g
100.41356206083556,-0.986163589,0.053049132227897644,0.17280970606952906,1,1,40.41356206083555,104.7189904,6,8.271241216711115,0.001,69.3,79.3,89.3,39.3,49.3,59.3,99.3,109.3,119.3,9.3,19.3,29.3,-0.039668731,-1.017069544,-0.07443793

'''

import csv
import socket

# load the data
data = []
with open('sample_vehicle_data_6kph.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row)

# create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send the data
for row in data:
    message = ','.join(row).encode()
    sock.sendto(message, ('localhost', 12345))
    print('sent:', message)

# close the socket
sock.close()

