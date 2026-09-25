import paho.mqtt.client as mqtt
from datetime import datetime, timezone
from sfunctions.func import mqtt_env

"""
print(mqtt_env("MQTT_HOST"))
print(mqtt_env("MQTT_PORT"))
print(mqtt_env("MQTT_USER"))
print(mqtt_env("MQTT_PASSWORD"))
print(mqtt_env('MQTT_TOPIC'))
print(mqtt_env('MQTT_CLIENT_ID'))
print(mqtt_env('MQTT_KEEPALIVE'))
print(mqtt_env('MQTT_QOS'))


Work to be implemented:
    1. Secure/stable/reconnections/industrial/simple connections for MQTT   (consider asyncio, thread)
    2. Write received data to the log file "data/YEAR/MONTH.log"            (consider asyncio, thread)
        Create data base column ID, date_utc, date_local, topic, value
    3. Delete the log from the previos year "data/YEAR-1"                   (consider asyncio, thread)
    4. Save data to POSTGRESQL                                              (consider asyncio, thread)
"""

# 1. Conexion segura/estable/reconexion/industrial/simple para mqttt  (valorar asyncio, thread)
def on_message(client, userdata, message):
    date_utc   = datetime.now(timezone.utc)
    date_local = date_utc.astimezone()
    topic      = message.topic
    content    = message.payload.decode("utf-8", errors="replace",)

    print(f"{str(date_utc)[:23]}")
    print(f"{str(date_local)[:23]}")
    print(f"[{topic}]")
    print(f"{content}")
    print("")

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code != 0:
        print(f"Conexion rechazada {reason_code}")
        return

    result, mId = client.subscribe(mqtt_env('MQTT_TOPIC'), qos=int(mqtt_env('MQTT_QOS')))

    if result != mqtt.MQTT_ERR_SUCCESS:
        print(f"Error al suscribirse {result}")


cliente = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id=mqtt_env('MQTT_CLIENT_ID'), clean_session=False, protocol=mqtt.MQTTv311,)
cliente.username_pw_set(username=mqtt_env("MQTT_USER"), password=mqtt_env("MQTT_PASSWORD"))
cliente.reconnect_delay_set(min_delay=1, max_delay=60)
cliente.connect_async(host=mqtt_env("MQTT_HOST"), port=int(mqtt_env('MQTT_PORT')), keepalive=30,)
cliente.on_connect = on_connect
cliente.on_message = on_message
cliente.loop_forever(retry_first_connection=True)

cliente.loop_forever()
