from pathlib import Path
from dotenv import dotenv_values
import paho.mqtt.client as mqtt

base_dir    = Path(__file__).resolve().parent.parent
config_file = base_dir / ".env"
config_app  = dotenv_values(config_file)

MQTT_HOST   = config_app.get('MQTT_HOST')


print(base_dir )
print(config_file)
print(config_app)
print(MQTT_HOST)
print(get_env())


"""
BROKER = "192.168.14.11"
PORT   = 1884

# USUARIO = "test"
# CONTRASENA = "pw"

USUARIO        = "xxx"
CONTRASENA     = "xxx"

TOPIC = "Froxa/#"


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