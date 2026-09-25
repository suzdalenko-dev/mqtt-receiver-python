from pathlib import Path
import queue, threading, json

DATA_DIRECTORY = Path(__file__).resolve().parent.parent.parent / "data"
LOG_QUEUE      = queue.Queue(maxsize=11111)


def getMi():
   # /opt/mqtt-receiver-python/data
   PROJECT_DIR = Path(__file__).resolve().parent.parent.parent / "data"
   print(PROJECT_DIR)
   return PROJECT_DIR


def put_message_to_log(date_utc, date_local, topic, content):
    message = {'date_utc': date_utc, 'date_local': date_local, 'topic': topic, 'content': content}
    try: 
        LOG_QUEUE.put_nowait(message)
    except Exception as error:
        print(f"Log queue full {error}")
    
    
def write_message_to_log(message):
    file_url = DATA_DIRECTORY / f"{date_utc.year:04d}" / f"{date_utc.month:02d}.log"
    date_utc = message['date_utc']

    message['date_utc']   = str(message['date_utc'])[:23]
    message['date_local'] = str(message['date_local'])[:23]

    json_line = json.dumps(message, ensure_ascii=False, separators=(',', ':'))
    with file_url.open(mode='a', encoding='utf-8',) as file:
        file.write(json_line)
        file.write('\n')
        file.flush()
        print(message)


def log_writer():
    while True:
        current_message = LOG_QUEUE.get()
        try:
            write_message_to_log(current_message)
        except Exception as e:
            print(f"Error write_message_to_log {e}")
        finally:
            LOG_QUEUE.task_done()


def start_log_writer() -> threading.Thread:
    tread = threading.Thread(target=log_writer, daemon=True,)
    tread.start()
    return tread