import json
import ssl
from pathlib import Path
import paho.mqtt.client as mqtt


BROKER         = "192.168.14.11"
PORT           = 8883
USUARIO        = "froxa"
CONTRASENA     = "O8wTi8GcsZ]R8-"
CERTIFICADO_CA = (Path(__file__).resolve().parent.parent / "config" / "ca.crt")
TOPIC          = "Froxa/#"

def on_message(client, userdata, message):
    contenido = message.payload.decode(
        "utf-8",
        errors="replace",
    )
    print(contenido)
    print(
        # f"[{message.topic}] "
        f"retain={message.retain} "
        #  f"qos={message.qos} "
        # f"{contenido}"
    )

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conexión MQTT correcta")
        client.subscribe(TOPIC, qos=0)
        print(f"Solicitada suscripción a: {TOPIC}")
    else:
        print(f"Conexión MQTT rechazada: {reason_code}")
        client.disconnect()


cliente = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="froxa",
    protocol=mqtt.MQTTv311,
)

cliente.username_pw_set(USUARIO, CONTRASENA)

cliente.tls_set(
    ca_certs=str(CERTIFICADO_CA),
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS_CLIENT,
)

cliente.on_connect = on_connect
cliente.on_message = on_message

cliente.connect(BROKER, PORT, keepalive=30)
cliente.loop_forever()