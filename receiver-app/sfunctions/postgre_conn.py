import threading
from contextlib import contextmanager
from psycopg_pool import ConnectionPool
from sfunctions.func import mqtt_env, reconnect_failed

# ============================================================
# SINGLETON POSTGRESQL CONNECTION POOL
# ============================================================

_pool: ConnectionPool | None = None
_pool_lock = threading.Lock()


def get_postgres_pool() -> ConnectionPool:
    global _pool

    # Fast path.
    # Almost every call will finish here after initialization.
    if _pool is not None and not _pool.closed:
        return _pool

     # Only needed during creation/recreation.
    with _pool_lock:

        # Another thread could have created it while we waited
        # for the lock, so check again.
        if _pool is None or _pool.closed:

            _pool = ConnectionPool(
                conninfo="",

                kwargs=connection_config(),

                # We want one persistent physical connection.
                min_size=1,
                max_size=1,

                # Explicitly open below.
                open=False,

                # Maximum time a caller waits to receive
                # a usable connection from the pool.
                timeout=5,

                # Period during which the pool retries using
                # exponential backoff before calling
                # _reconnect_failed().
                reconnect_timeout=60,

                reconnect_failed=reconnect_failed,

                # Check the connection before giving it to us.
                check=ConnectionPool.check_connection,

                # Replace connections periodically.
                max_lifetime=22771,

                name="mqtt-postgres",
            )

            # Important:
            # don't block MQTT startup waiting for PostgreSQL.
            #
            # The pool connects/reconnects in its background worker.
            _pool.open(wait=False)

    return _pool




@contextmanager
def postgres_connection():
    """
    Obtain a healthy PostgreSQL connection.

    On success:
        transaction COMMIT
        connection returns to the pool.

    On exception:
        transaction ROLLBACK
        connection returns to the pool or is replaced if broken.
    """
    pool = get_postgres_pool()

    with pool.connection() as connection:
        yield connection



def close_postgres_pool():
    """
    Gracefully close PostgreSQL connections.

    Intended for application shutdown.
    """
    global _pool

    with _pool_lock:

        if _pool is not None:
            _pool.close(timeout=5)
            _pool = None
