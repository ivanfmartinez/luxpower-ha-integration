import asyncio
import logging

from ..classes.lxp_request_builder import LxpRequestBuilder
from ..classes.lxp_response import LxpResponse
from ..const import DOMAIN, WRITE_RESPONSE_LENGTH, MAX_RETRIES

_LOGGER = logging.getLogger(__name__)


async def write_register(hass, entry, register, value):
    """Write a single register value to the inverter using info from config entry."""
    lock = hass.data[DOMAIN][entry.entry_id].get("lock")

    for attempt in range(MAX_RETRIES):
        async with lock:
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

                response_buf = await reader.read(WRITE_RESPONSE_LENGTH)

                _LOGGER.debug(
                    "Modbus WRITE: Sent to reg %s, value %s, resp: %s",
                    register, value, response_buf.hex()
                )

                writer.close()
                await writer.wait_closed()

                # 1. Check response length
                if not response_buf:
                    _LOGGER.warning(
                        "Write attempt %d failed: No response",
                        attempt + 1)
                    await asyncio.sleep(1)  # Wait a second before retrying
                    continue

                # 2. Check for packet errors
                response = LxpResponse(response_buf)
                if response.packet_error:
                    _LOGGER.warning("Write attempt %d failed: Inverter returned a packet error.", attempt + 1)
                    await asyncio.sleep(1)
                    continue

                # 3. Confirm the inverter echoed back the correct register and value
                # This assumes LxpResponse can parse a write-ack correctly
                response_dict = response.parsed_values_dictionary

                sent_int = int(value)
                received_int = int(response_dict.get(register))
                if response.register == register and sent_int == received_int:
                    _LOGGER.debug("Successfully wrote register %s with value %s.", register, value)
                    return True  # Success! Exit the function.
                else:
                    _LOGGER.warning(
                        "Write attempt %d failed: Confirmation mismatch. Sent reg %s with value %s, but inverter responded with reg %s, value %s.",
                        attempt + 1, register, value, response.register, response_dict.get(register)
                    )
                    await asyncio.sleep(1)
                    continue

            except Exception as ex:
                _LOGGER.error("Exception during write attempt %d for register %s: %s", attempt + 1, register, ex)
                await asyncio.sleep(1)  # Wait before the next attempt

    # If the loop finishes without returning True, all retries have failed
    _LOGGER.error("Failed to write register %s after %d attempts.", register, MAX_RETRIES)
    return False
