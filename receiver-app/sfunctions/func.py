from pathlib import Path
from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = BASE_DIR / ".env"
CONFIG_APP = dotenv_values(CONFIG_FILE)


def mqtt_env(tag):
    return CONFIG_APP.get(tag)


def critical_db_writer():
    """
    Wrapper for the critical DB writer thread.

    If db_writer() dies unexpectedly, terminate the
    complete Python process so Docker/systemd can restart it.
    """

    try:

        db_writer()

    except BaseException as e:

        print(
            f"CRITICAL: postgres-db-writer died: {e}",
            flush=True,
        )

        os._exit(1)

    # db_writer() is expected to run forever.
    # If it returns normally, this is also considered critical.
    print(
        "CRITICAL: postgres-db-writer finished unexpectedly",
        flush=True,
    )

    os._exit(1)