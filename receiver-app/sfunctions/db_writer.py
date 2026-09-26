import queue, json, threading

DB_QUEUE      = queue.Queue(maxsize=11111)


def insert_date_to_db(m):
    pass



def put_message_to_db_queue(date_utc, date_local, topic, content):
    global DB_QUEUE
    date_utc   = str(date_utc)[:23]
    date_local = str(date_local)[:23]
    try:
        content = json.loads(content)
    except:
            content = content
    
    message = {'date_utc':date_utc, 'date_local':date_local, 'topic':topic, 'content':content}
    try:
        DB_QUEUE.put_nowait(message)
    except Exception as e:
        print(f"Error insert data to db queue {e}")



def db_writer():
    global DB_QUEUE
    while True:
        try:
            m = DB_QUEUE.get()
            insert_date_to_db(m)
        except Exception as e:
            print(f"Error insert data to DB {e}")
        finally:
            DB_QUEUE.task_done()
             
     

def start_db_inserter():
    thread = threading.Thread(
    target=db_writer,
    name="postgres-db-writer",
    daemon=True,
)