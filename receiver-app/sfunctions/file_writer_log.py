from pathlib import Path
import queue, threading, json, shutil, os

DATA_DIRECTORY = Path(__file__).resolve().parent.parent.parent / "data"
LOG_QUEUE      = queue.Queue(maxsize=11111)



def put_message_to_log(date_utc, date_local, topic, content):
    try:
        content = json.loads(content)
    except:
        content = content
    message = {'date_utc': date_utc, 'date_local': date_local, 'topic': topic, 'content': content}
    try: 
        LOG_QUEUE.put_nowait(message)
    except Exception as error:
        print(f"Log queue full {error}")
    
    
def write_message_to_log(message):
    date_utc    = message['date_utc']
    year_minus1 = date_utc.year - 1
    year_dir    = DATA_DIRECTORY / f"{date_utc.year:04d}"
    year_dir.mkdir(parents=True, exist_ok=True)
    file_url    = DATA_DIRECTORY / f"{date_utc.year:04d}" / f"{date_utc.month:02d}.log"
    
    message['date_utc']   = str(message['date_utc'])[:23]
    message['date_local'] = str(message['date_local'])[:23]

    json_line = json.dumps(message, ensure_ascii=False, separators=(',', ':'))
    with file_url.open(mode='a', encoding='utf-8',) as file:
        file.write(json_line)
        file.write('\n')
        file.flush()

    year_dir = DATA_DIRECTORY / str(year_minus1)
    try:
        if year_dir.exists() and year_dir.is_dir():
            shutil.rmtree(year_dir)
    except Exception as e:
        print(f"Error when intent delete old directory {e}")


def log_writer():
    while True:
        current_message = LOG_QUEUE.get()
        try:
            write_message_to_log(current_message)
        except Exception as e:
            print(f"Error write_message_to_log {e}")
        finally:
            LOG_QUEUE.task_done()


def critical_log_writer():
    try:
        log_writer()
    except BaseException as e:
        print(
            f"CRITICAL: postgres-db-writer died: {e}",
            flush=True,
        )
        os._exit(1)


def start_log_writer() -> threading.Thread:
    tread = threading.Thread(target=critical_log_writer, daemon=True,)
    tread.start()
    return tread