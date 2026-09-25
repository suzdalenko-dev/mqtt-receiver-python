import asyncio
import logging
from datetime import datetime

from asyncua import Client, ua


OPCUA_URL = "opc.tcp://192.xxx.xxx.xxx:4840"
NODE_ID_PREFIX = "ns=2;s=CPS-MCS341-DS.STAG."

# Intervalo solicitado al servidor, en milisegundos.
INTERVALO_MS = 222

TAGS = [
    "STAG00", "STAG01", "STAG02",
    "STAG10", "STAG11", "STAG12", "STAG13", "STAG14",
    "STAG21", "STAG22", "STAG23", "STAG24", "STAG25", "STAG26",
    "STAG27", "STAG28", "STAG29", "STAG30", "STAG31", "STAG32",
    "STAG33", "STAG34", "STAG35", "STAG36", "STAG37", "STAG38",
    "STAG39", "STAG53",
]


class MostrarCambios:
    def __init__(self, tags_por_node_id):
        self.tags_por_node_id = tags_por_node_id

    def datachange_notification(self, node, valor, data):
        """Se ejecuta cuando llega una notificación de un tag."""
        node_id = node.nodeid.to_string()
        tag = self.tags_por_node_id.get(node_id, node_id)
        dato = data.monitored_item.Value

        recibido = datetime.now().astimezone().isoformat(
            timespec="milliseconds"
        )

        # !r muestra también las comillas y los espacios del valor recibido.
        print(
            f"{recibido} | {tag} "
            f"| valor={valor!r} "
            f"| calidad={dato.StatusCode.name} "
            f"| origen={dato.SourceTimestamp}",
            flush=True,
        )

    def status_change_notification(self, notification):
        logging.warning(
            "Estado de la suscripción: %s",
            notification.Status.name,
        )


async def avisar_desconexion(error):
    logging.warning(
        "Conexión perdida: %r. Intentando reconectar...",
        error,
    )


async def escuchar():
    print(f"\nConectando a {OPCUA_URL}...", flush=True)

    client = Client(
        url=OPCUA_URL,
        timeout=22,
        watchdog_intervall=5,
        auto_reconnect=True,
        reconnect_max_delay=30,
    )

    client.connection_lost_callback = avisar_desconexion

    async with client:
        print("Sesión OPC UA establecida.", flush=True)

        nodos_por_tag = {
            tag: client.get_node(f"{NODE_ID_PREFIX}{tag}")
            for tag in TAGS
        }

        tags_por_node_id = {
            node.nodeid.to_string(): tag
            for tag, node in nodos_por_tag.items()
        }

        handler = MostrarCambios(tags_por_node_id)

        subscription = await client.create_subscription(
            INTERVALO_MS,
            handler,
        )

        resultados = await subscription.subscribe_data_change(
            list(nodos_por_tag.values()),
            queuesize=1000,
            sampling_interval=INTERVALO_MS,
        )

        # Verificar que el servidor ha aceptado todos los tags.
        for tag, resultado in zip(TAGS, resultados, strict=True):
            if isinstance(resultado, ua.StatusCode):
                raise RuntimeError(
                    f"No se pudo suscribir {tag}: {resultado.name}"
                )

        print(
            f"\nEscuchando {len(TAGS)} tags. "
            "Pulsa Ctrl+C para detener.\n",
            flush=True,
        )

        # Mantener la sesión abierta mientras las tareas de asyncua
        # reciben notificaciones y gestionan la reconexión.
        await asyncio.Event().wait()


async def main():
    while True:
        try:
            await escuchar()
        except asyncio.CancelledError:
            # Permitir la parada y el cierre de la conexión.
            raise
        except Exception:
            logging.exception(
                "Error iniciando el monitor. Reintentando en 5 segundos."
            )
            await asyncio.sleep(5)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s %(levelname)s: %(message)s",
    )

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitor detenido.")