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



def on_message(client, userdata, message):
    contenido = message.payload.decode("utf-8", errors="replace",)

    print(f"[{message.topic}] retain={message.retain}  {contenido}")



def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conexión MQTT correcta sin TLS")

        client.subscribe(TOPIC, qos=0)
        print(f"Suscrito a: {TOPIC}")

    else:
        print(f"Conexión MQTT rechazada: {reason_code}")
        client.disconnect()


cliente = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="froxa-sin-tls",
    protocol=mqtt.MQTTv311,
)

cliente.username_pw_set(
    username=USUARIO,
    password=CONTRASENA,
)

cliente.on_connect = on_connect
cliente.on_message = on_message

cliente.connect(
    host=BROKER,
    port=PORT,
    keepalive=30,
)

cliente.loop_forever()
"""