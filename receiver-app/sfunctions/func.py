from pathlib import Path
from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = BASE_DIR / ".env"
CONFIG_APP = dotenv_values(CONFIG_FILE)


def mqtt_env(tag):
    return CONFIG_APP.get(tag)

