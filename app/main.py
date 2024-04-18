from udp_listener import udp_listener
from msg_processor import process, create_db
from multiprocessing import Queue, Process

def test_q_append(q: Queue):
    q.put("a message")


if __name__ == "__main__":
    create_db()
    q1 = Queue()
    q2 = Queue()
    listener = Process(target=udp_listener, args=[q1, q2])
    processor = Process(target=process, args=[q1, q2])

    listener.start()
    processor.start()