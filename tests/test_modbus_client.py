import asyncio
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from custom_components.lxp_modbus.classes.modbus_client import LxpModbusApiClient

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
        block_size=2
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
    response_instance.serial_number = "DUMMY00001".encode()
    # Use unique values for each test
    parsed_values = {i: i*10 for i in range(1, 3)}
    response_instance.parsed_values_dictionary = parsed_values
    mock_response.return_value = response_instance
    input_bytes = bytes.fromhex(response_dict["response_hex"])
    reader.read = AsyncMock(side_effect=[input_bytes, input_bytes])

    with (
        patch("custom_components.lxp_modbus.classes.modbus_client.TOTAL_REGISTERS", 2),
        patch("custom_components.lxp_modbus.classes.modbus_client.REGISTER_BLOCK_SIZE", 2),
        patch("custom_components.lxp_modbus.classes.modbus_client.RESPONSE_OVERHEAD", 0)
    ):
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
    response_instance.serial_number = "DUMMY00001".encode()
    parsed_values = {i: i*100 for i in range(1, 3)}
    response_instance.parsed_values_dictionary = parsed_values
    mock_response.return_value = response_instance
    hold_bytes = bytes.fromhex(response_dict["response_hex"])
    reader.read = AsyncMock(side_effect=[hold_bytes, hold_bytes])

    with (
        patch("custom_components.lxp_modbus.classes.modbus_client.TOTAL_REGISTERS", 2),
        patch("custom_components.lxp_modbus.classes.modbus_client.REGISTER_BLOCK_SIZE", 2),
        patch("custom_components.lxp_modbus.classes.modbus_client.RESPONSE_OVERHEAD", 0)
    ):
        result = asyncio.run(api_client.async_get_data())
        assert result["input"] == parsed_values
        assert result["hold"] == parsed_values
