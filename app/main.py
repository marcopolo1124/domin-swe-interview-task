from udp_listener import udp_listener
from msg_processor import process_db, create_db
from multiprocessing import Queue, Process

def test_q_append(q: Queue):
    q.put("a message")


if __name__ == "__main__":
    create_db()
    q = Queue()
    listener = Process(target=udp_listener, args=[q])
    processor = Process(target=process_db, args=[q])

    listener.start()
    processor.start()