import asyncio
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from custom_components.lxp_modbus.classes.modbus_client import LxpModbusApiClient
from custom_components.lxp_modbus.const import TOTAL_REGISTERS, RESPONSE_OVERHEAD

# Import dummy data
from tests.test_data import INPUT_RESPONSES, HOLD_RESPONSES

DUMMY_HOST = "127.0.0.1"
DUMMY_PORT = 8000

@pytest.fixture
def api_client():
    lock = asyncio.Lock()
    return LxpModbusApiClient(
        host=DUMMY_HOST,
        port=DUMMY_PORT,
        dongle_serial="DUMMY_DONGLE",
        inverter_serial="DUMMY00001",
        lock=lock,
        block_size=1,  # Use block size 1 for easier testing
        skip_initial_data=False
    )


import itertools

@pytest.mark.parametrize("response_key,response_dict", INPUT_RESPONSES.items())
@patch("custom_components.lxp_modbus.classes.modbus_client.asyncio.open_connection")
@patch("custom_components.lxp_modbus.classes.modbus_client.LxpRequestBuilder")
@patch("custom_components.lxp_modbus.classes.modbus_client.LxpResponse")
def test_async_get_data_input_response(mock_response, mock_builder, mock_open_conn, api_client, response_key, response_dict):
    reader = MagicMock()
    writer = MagicMock()
    writer.drain = AsyncMock()
    writer.close = AsyncMock()
    writer.wait_closed = AsyncMock()
    mock_open_conn.return_value = (reader, writer)
    mock_builder.prepare_packet_for_read.return_value = b"request"
    
    # Simulate valid response
    response_instance = MagicMock()
    response_instance.packet_error = False
    response_instance.serial_number = api_client._inverter_serial.encode()
    response_instance.device_function = 4
    parsed_values = {i: i*10 for i in range(1, 3)}
    response_instance.parsed_values_dictionary = parsed_values
    mock_response.return_value = response_instance
    
    # Make read return the same input_bytes for every call
    input_bytes = bytes.fromhex(response_dict["response_hex"])
    reader.read = AsyncMock()
    reader.read.return_value = input_bytes

    # Use a small register count and no overhead for simple testing
    with patch("custom_components.lxp_modbus.const.TOTAL_REGISTERS", 1), patch("custom_components.lxp_modbus.const.RESPONSE_OVERHEAD", 0):
        result = asyncio.run(api_client.async_get_data())
        assert result["input"] == parsed_values
        assert result["hold"] == parsed_values


@pytest.mark.parametrize("response_key,response_dict", HOLD_RESPONSES.items())
@patch("custom_components.lxp_modbus.classes.modbus_client.asyncio.open_connection")
@patch("custom_components.lxp_modbus.classes.modbus_client.LxpRequestBuilder")
@patch("custom_components.lxp_modbus.classes.modbus_client.LxpResponse")
def test_async_get_data_hold_response(mock_response, mock_builder, mock_open_conn, api_client, response_key, response_dict):
    reader = MagicMock()
    writer = MagicMock()
    writer.drain = AsyncMock()
    writer.close = AsyncMock()
    writer.wait_closed = AsyncMock()
    mock_open_conn.return_value = (reader, writer)
    mock_builder.prepare_packet_for_read.return_value = b"request"
    
    # Simulate valid response
    response_instance = MagicMock()
    response_instance.packet_error = False
    response_instance.serial_number = api_client._inverter_serial.encode()
    response_instance.device_function = 3
    parsed_values = {i: i*100 for i in range(1, 3)}
    response_instance.parsed_values_dictionary = parsed_values
    mock_response.return_value = response_instance
    
    # Make read return the same hold_bytes for every call
    hold_bytes = bytes.fromhex(response_dict["response_hex"])
    reader.read = AsyncMock()
    reader.read.return_value = hold_bytes

    # Use a small register count and no overhead for simple testing
    with patch("custom_components.lxp_modbus.const.TOTAL_REGISTERS", 1), patch("custom_components.lxp_modbus.const.RESPONSE_OVERHEAD", 0):
        result = asyncio.run(api_client.async_get_data())
        assert result["input"] == parsed_values
        assert result["hold"] == parsed_values
