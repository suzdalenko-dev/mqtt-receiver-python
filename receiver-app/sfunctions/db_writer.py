import queue, json, threading
from sfunctions.postgre_conn import postgres_connection

DB_QUEUE      = queue.Queue(maxsize=11111)


def insert_date_to_db(m):
    """
    Insert one MQTT message into PostgreSQL.
    """

    sql = """
        INSERT INTO public.mqtt_record_lines (date_utc, date_local, topic, content)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (date_utc)
        DO NOTHING
    """

    with postgres_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (m["date_utc"], m["date_local"], m["topic"], m["content"],))




def put_message_to_db_queue(date_utc, date_local, topic, content):
    global DB_QUEUE
    date_utc   = str(date_utc)[:23]
    date_local = str(date_local)[:23]
    try:
        content = json.loads(content)
    except:
        content = content
    message = {'date_utc':date_utc, 'date_local':date_local, 'topic':topic, 'content':str(content)}
    try:
        DB_QUEUE.put_nowait(message)
    except Exception as e:
        print(f"Error insert data to db queue {e}")



def db_writer():
    global DB_QUEUE
    while True:
        m = DB_QUEUE.get()
        try:
            while True:
                try:
                    insert_date_to_db(m)
                    break
                except Exception as e:
                    print(f"Error in insert_date_to_db function {e}")
        except Exception as e:
            print(f"Error insert data to DB {e}")
        finally:
            DB_QUEUE.task_done()
             
     

def start_db_inserter():
    thread = threading.Thread(target=db_writer, name="postgres-db-writer", daemon=True,)
    thread.start()