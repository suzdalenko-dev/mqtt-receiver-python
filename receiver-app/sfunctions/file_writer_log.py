from pathlib import Path
import queue, threading


LOG_QUEUE = queue.Queue(maxsize=11111)


def getMi():
   # /opt/mqtt-receiver-python/data
   PROJECT_DIR = Path(__file__).resolve().parent.parent.parent / "data"
   print(PROJECT_DIR)
   return PROJECT_DIR

def log_writer():
    while True:
        current_event = LOG_QUEUE.get()
        print('log_writer')


def start_log_writer() -> threading.Thread:
    tread = threading.Thread(target=log_writer, daemon=True,)
    tread.start()
    return tread