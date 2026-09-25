import paho.mqtt.client as mqtt
from sfunctions.func import mqtt_env


print(mqtt_env("MQTT_HOST"))
print(mqtt_env("MQTT_PORT"))
print(mqtt_env("MQTT_USER"))
print(mqtt_env("MQTT_PASSWORD"))
print(mqtt_env('MQTT_TOPIC'))
print(mqtt_env('MQTT_CLIENT_ID'))
print(mqtt_env('MQTT_KEEPALIVE'))
print(mqtt_env('MQTT_QOS'))



"""
Trabajo a implementar:
    1. Conexion segura/estable/reconexion/industrial/simple para mqttt  (valorar asyncio, thread)
    2. Escritura en de log datos recibidos "data/YEAR/MONTH.log"        (valorar asyncio, thread)
    3. Borrado de log del año anterior "data/YEAR-1"                    (valorar asyncio, thread)
    4. Guardar datos en POSTGRESQL                                      (valorar asyncio, thread)
"""

def on_message(client, userdata, message):
    content = message.payload.decode("utf-8", errors="replace",)
    print(f"[{message.topic}] retain={message.retain}  {content}")

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conexión MQTT correcta sin TLS")

        client.subscribe(mqtt_env('MQTT_TOPIC'), qos=0)
        print(f"Suscrito a: {mqtt_env('MQTT_TOPIC')}")

    else:
        print(f"Conexión MQTT rechazada: {reason_code}")
        client.disconnect()


cliente = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id=mqtt_env('MQTT_CLIENT_ID'), protocol=mqtt.MQTTv311,)
cliente.username_pw_set(username=mqtt_env("MQTT_USER"), password=mqtt_env("MQTT_PASSWORD"),)
cliente.on_connect = on_connect
cliente.on_message = on_message
cliente.connect(host=mqtt_env("MQTT_HOST"), port=1884, keepalive=30,)

cliente.loop_forever()
