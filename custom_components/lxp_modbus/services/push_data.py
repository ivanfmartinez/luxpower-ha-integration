import asyncio
import logging

from ..classes.lxp_request_builder import LxpRequestBuilder

_LOGGER = logging.getLogger(__name__)

async def write_register(hass, entry, register, value):
    """Write a single register value to the inverter using info from config entry."""
    try:
        host = entry.data["host"]
        port = entry.data.get("port", 8000)
        dongle_serial = entry.data["dongle_serial"].encode()
        inverter_serial = entry.data["inverter_serial"].encode()

        reader, writer = await asyncio.open_connection(host, port)

        req = LxpRequestBuilder.prepare_packet_for_write(
            dongle_serial, inverter_serial, register, value
        )
        writer.write(req)
        await writer.drain()

        response = await reader.read(512)
        _LOGGER.debug(
            "Modbus WRITE: Sent to reg %s, value %s, resp: %s",
            register, value, response.hex()
        )

        writer.close()
        await writer.wait_closed()
        return True

    except Exception as ex:
        _LOGGER.error("Error writing register %s: %s", register, ex)
        return False