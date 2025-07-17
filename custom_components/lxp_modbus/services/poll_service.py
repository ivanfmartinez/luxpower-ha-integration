import asyncio
import logging

from homeassistant.helpers.dispatcher import async_dispatcher_send
from ..const import DOMAIN, REGISTER_BLOCK_SIZE, TOTAL_REGISTERS, SIGNAL_REGISTER_UPDATED,RESPONSE_LENGTH_EXPECTED
from ..classes.lxp_request_builder import LxpRequestBuilder
from ..classes.lxp_response import LxpResponse

_LOGGER = logging.getLogger(__name__)

async def poll_inverter_task(hass, entry, host, port, dongle_serial, inverter_serial, poll_interval):
    """Poll inverter for INPUT and HOLD registers in a loop."""
    last_input_values = {}
    last_hold_values = {}
    hass.data[DOMAIN][entry.entry_id]['initialized'] = False
    
    if 'registers' not in hass.data[DOMAIN][entry.entry_id]:
        hass.data[DOMAIN][entry.entry_id]['registers'] = { "input": {}, "hold": {} }

    while True:
        _LOGGER.debug("Polling inverter at %s:%s", host, port)
        
        input_poll_ok = True
        hold_poll_ok = True
        
        new_input_values = {}
        new_hold_values = {}

        try:
            reader, writer = await asyncio.open_connection(host, port)

            # --- INPUT REGISTERS (function code 4) ---
            for reg in range(0, TOTAL_REGISTERS, REGISTER_BLOCK_SIZE):
                count = min(REGISTER_BLOCK_SIZE, TOTAL_REGISTERS - reg)
                req = LxpRequestBuilder.prepare_packet_for_read(dongle_serial, inverter_serial, reg, count, 4)
                writer.write(req)
                await writer.drain()
                response_buf = await reader.read(RESPONSE_LENGTH_EXPECTED)
                
                if not response_buf or len(response_buf) != RESPONSE_LENGTH_EXPECTED:
                    input_poll_ok = False
                    _LOGGER.warning(
                        "Invalid response length for INPUT %d-%d. Got %d bytes, expected %d.",
                        reg, reg + count - 1, len(response_buf) if response_buf else 0, RESPONSE_LENGTH_EXPECTED
                    )
                    continue

                response = LxpResponse(response_buf)
                if not response.packet_error:
                    new_input_values.update(response.parsed_values_dictionary)
                else:
                    input_poll_ok = False
                    _LOGGER.warning("Packet error for INPUT %d-%d", reg, reg + count - 1)
                    continue
            
            # --- HOLD REGISTERS (function code 3) ---
            for reg in range(0, TOTAL_REGISTERS, REGISTER_BLOCK_SIZE):
                count = min(REGISTER_BLOCK_SIZE, TOTAL_REGISTERS - reg)
                req = LxpRequestBuilder.prepare_packet_for_read(dongle_serial, inverter_serial, reg, count, 3)
                writer.write(req)
                await writer.drain()
                response_buf = await reader.read(RESPONSE_LENGTH_EXPECTED)

                if not response_buf or len(response_buf) != RESPONSE_LENGTH_EXPECTED:
                    hold_poll_ok = False
                    _LOGGER.warning(
                        "Invalid response length for HOLD %d-%d. Got %d bytes, expected %d.",
                        reg, reg + count - 1, len(response_buf) if response_buf else 0, RESPONSE_LENGTH_EXPECTED
                    )

                    continue

                response = LxpResponse(response_buf)
                if not response.packet_error:
                    new_hold_values.update(response.parsed_values_dictionary)
                else:
                    hold_poll_ok = False
                    _LOGGER.warning("Packet error for HOLD %d-%d", reg, reg + count - 1)
                    continue

            writer.close()
            await writer.wait_closed()

        except Exception as ex:
            _LOGGER.warning("Polling connection error: %s", ex)
            input_poll_ok = False
            hold_poll_ok = False
        
        if input_poll_ok:
            _LOGGER.debug("Input poll successful. Updating state.")
            hass.data[DOMAIN][entry.entry_id]['registers']["input"] = new_input_values
            for reg, new_val in new_input_values.items():
                if last_input_values.get(reg) != new_val:
                    # Using the required thread-safe call
                    hass.loop.call_soon_threadsafe(
                        async_dispatcher_send, hass, SIGNAL_REGISTER_UPDATED, entry.entry_id, "input", reg, new_val
                    )
            last_input_values = new_input_values
        else:
            _LOGGER.warning("Input poll failed. Keeping old input register values.")

        if hold_poll_ok:
            _LOGGER.debug("Hold poll successful. Updating state.")
            hass.data[DOMAIN][entry.entry_id]['registers']["hold"] = new_hold_values
            for reg, new_val in new_hold_values.items():
                if last_hold_values.get(reg) != new_val:
                    # Using the required thread-safe call
                    hass.loop.call_soon_threadsafe(
                        async_dispatcher_send, hass, SIGNAL_REGISTER_UPDATED, entry.entry_id, "hold", reg, new_val
                    )
            last_hold_values = new_hold_values
        else:
            _LOGGER.warning("Hold poll failed. Keeping old hold register values.")

        if not hass.data[DOMAIN][entry.entry_id]['initialized']:
            if input_poll_ok and hold_poll_ok:
                _LOGGER.info("First successful poll complete. Marking as initialized.")
                hass.data[DOMAIN][entry.entry_id]['initialized'] = True
        
        await asyncio.sleep(poll_interval)