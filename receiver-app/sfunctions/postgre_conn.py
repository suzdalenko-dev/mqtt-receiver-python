import threading
from contextlib import contextmanager
from psycopg_pool import ConnectionPool
from sfunctions.func import mqtt_env


# ============================================================
# SINGLETON POSTGRESQL CONNECTION POOL
# ============================================================

_pool: ConnectionPool | None = None
_pool_lock = threading.Lock()


def _required_env(name: str) -> str:
    """
    Read a required configuration value from .env.

    If the value doesn't exist or is empty, fail immediately.
    """
    value = mqtt_env(name)

    if value is None or str(value).strip() == "":
        raise RuntimeError(
            f"Missing required environment variable: {name}"
        )

    return str(value).strip()


def _connection_config() -> dict:
    """
    PostgreSQL connection configuration.
    """
    return {
        "host": _required_env("POSTGRES_HOST"),
        "port": int(_required_env("POSTGRES_PORT")),
        "dbname": _required_env("POSTGRES_DB"),
        "user": _required_env("POSTGRES_USER"),
        "password": _required_env("POSTGRES_PASSWORD"),

        # Maximum time for each TCP/PostgreSQL connection attempt.
        "connect_timeout": 5,

        # Visible from PostgreSQL pg_stat_activity.
        "application_name": "mqtt-receiver-python",

        # Detect dead TCP connections.
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 3,
    }


def _reconnect_failed(pool: ConnectionPool):
    """
    Called when the pool has been unable to establish a
    PostgreSQL connection during reconnect_timeout.
    """
    print(
        f"PostgreSQL unavailable. "
        f"Pool '{pool.name}' continues trying to reconnect."
    )


def get_postgres_pool() -> ConnectionPool:
    """
    Return the single PostgreSQL ConnectionPool used by
    this Python process.

    First call:
        creates the pool.

    Following calls:
        reuse exactly the same pool.
    """
    global _pool

    # Normal/fast path.
    if _pool is not None and not _pool.closed:
        return _pool

    # Only one thread can create/recreate the pool.
    with _pool_lock:

        # Check again because another thread may have created
        # the pool while this thread was waiting for the lock.
        if _pool is None or _pool.closed:

            _pool = ConnectionPool(
                conninfo="",

                kwargs=_connection_config(),

                # One physical PostgreSQL connection.
                min_size=1,
                max_size=1,

                # We open it explicitly below.
                open=False,

                # Maximum time waiting to obtain a connection.
                timeout=5,

                # Retry failed connections before calling
                # _reconnect_failed().
                reconnect_timeout=60,

                reconnect_failed=_reconnect_failed,

                # Verify connection health before handing it out.
                check=ConnectionPool.check_connection,

                # Periodically renew old connections.
                max_lifetime=3600,

                name="mqtt-postgres",
            )

            # Start pool background workers.
            # Do not block application startup waiting for PostgreSQL.
            _pool.open(wait=False)

    return _pool


@contextmanager
def postgres_connection():
    """
    Obtain a PostgreSQL connection from the singleton pool.

    Successful block:
        COMMIT and return connection to pool.

    Exception:
        ROLLBACK and return/replace connection as appropriate.
    """
    pool = get_postgres_pool()

    with pool.connection() as connection:
        yield connection


def close_postgres_pool():
    """
    Gracefully close the PostgreSQL pool during application shutdown.
    """
    global _pool

    with _pool_lock:

        if _pool is not None:
            _pool.close(timeout=5)
            _pool = None