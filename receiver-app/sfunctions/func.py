from pathlib import Path
from dotenv import dotenv_values

base_dir    = Path(__file__).resolve().parent.parent.parent
config_file = base_dir / ".env"
config_app  = dotenv_values(config_file)

def mqtt_env(tag):
    value   = config_app.get(tag)
    return value


def reconnect_failed(pool: ConnectionPool):
    print(
        f"PostgreSQL connection unavailable. "
        f"Pool '{pool.name}' will continue reconnecting."
    )


def connection_config():
    pass