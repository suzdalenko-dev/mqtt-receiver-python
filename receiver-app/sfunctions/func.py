from pathlib import Path
from dotenv import dotenv_values


def get_env():
    base_dir    = Path(__file__).resolve().parent.parent
    config_file = base_dir / ".env"
    config_app  = dotenv_values(config_file)

    MQTT_HOST   = config_app.get('MQTT_HOST')
    return 'MQTT_HOST'




base_dir    = Path(__file__).resolve().parent.parent.parent
config_file = base_dir / ".env"
config_app  = dotenv_values(config_file)

MQTT_USER  = config_app.get('MQTT_USER')

MQTT_HOST   = config_app.get('HOST')
MQTT_PORT   = config_app.get('PORT')
MQTT_PASS   = config_app.get('PASS')
MQTT_TOPIC  = config_app.get('TOPIC')
MQTT_CLIENT = config_app.get('CLIENT')
MQTT_LOG    = config_app.get('LOGURL')