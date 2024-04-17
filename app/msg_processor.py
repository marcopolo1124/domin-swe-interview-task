from multiprocessing import Queue
import sqlite3
from sqlite3 import Cursor, Connection
import time

headers = "altitude,body_x_axis,body_y_axis,body_z_axis,fix,horizontal_dilution,latitude,longitude,num_sats,spd_over_grnd,timestamps,vehicle_accel_x,vehicle_accel_y,vehicle_accel_z,vehicle_gyro_x,vehicle_gyro_y,vehicle_gyro_z,vehicle_mag_x,vehicle_mag_y,vehicle_mag_z,vehicle_orientation_x,vehicle_orientation_y,vehicle_orientation_z,wheel_x_axis,wheel_y_axis,wheel_z_axis"
headers_list = headers.split(",")

def create_db():
    con = sqlite3.connect("suspensions.db")
    cursor = con.cursor()
    

    create_query = """CREATE TABLE IF NOT EXISTS suspension_data (
        id INTEGER PRIMARY KEY,
        time_inserted TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    """


    for header in headers_list:
        create_query += f"{header} REAL,"
    create_query += "archived BOOLEAN DEFAULT false);"
    print(create_query)
    cursor.execute(create_query)
    con.close()


def process_db(q: Queue):
    con = sqlite3.connect("suspensions.db")
    cursor = con.cursor()
    i = 0

    while True:
        insert_messages(cursor, q)
        if i % 30 == 0:
            send_and_archive(cursor, con)
        if i % 60 == 0:
            delete_archived(cursor, con)
        i = (i + 1) % 600
        time.sleep(1)

def insert_messages(cursor: Cursor, q: Queue):
    i = 0
    rows = 0
    insert_query = f"INSERT INTO suspension_data ({headers}) VALUES "
    while not q.empty() and i < 10000:
        msg = q.get()
        msg_lst = msg.split(",")
        
        if len(msg_lst) == len(headers_list):
            if rows > 0:
                insert_query += ","
            insert_query += f"({msg})"
            rows += 1
        i += 1
    if rows > 0:
        try:
            print("inserting")
            cursor.execute(insert_query)
            cursor.execute("COMMIT")
            print(f"rows added {rows}")
        except Exception as e:
            print("failed to insert new rows: ", e)
        

def send_to_database(rows):
    time.sleep(10)
    raise ConnectionError
        
def send_and_archive(cursor: Cursor, con: Connection):
    update_query = "UPDATE suspension_data SET archived = true WHERE archived = false RETURNING *;"
    try:
        cursor.execute(update_query)
        rows = cursor.fetchall()
        print(len(rows))

        send_to_database(rows)
        
        con.commit()
        print("sent to cloud")
    except Exception:
        print("rolling back")
        cursor.execute("ROLLBACK")
        

def delete_archived(cursor: Cursor, con: Connection):
    delete_query = """
    DELETE FROM suspension_data 
    WHERE archived = true and time_inserted < datetime('now', '-5 minutes')
    """
    try:
        print("deleting")
        cursor.execute(delete_query)
        con.commit()
        print("Successfully deleted")
    except Exception as e:
        print("Deletion unsuccessful: ", e)