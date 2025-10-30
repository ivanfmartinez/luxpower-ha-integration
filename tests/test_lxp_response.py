"""Tests for the LxpResponse class."""

import asyncio
import pytest

# Import the module under test
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from custom_components.lxp_modbus.classes.lxp_response import LxpResponse
from test_data import EXCEPTION_RESPONSES, FUNCTION_193_MESSAGE

class TestLxpResponse:
    """Test cases for LxpResponse."""

    @pytest.mark.asyncio
    async def test_exception_response_parsing(self):
        """Test exception response."""
        sample_exception_response = bytes.fromhex(EXCEPTION_RESPONSES["DUMMY_INVERTER_1_EXCEPTION"]["response_hex"])
        response = LxpResponse(sample_exception_response)
        print(response.info)
        
        assert response.packet_error is False
        assert response.dongle_serial == b"DG99999999"
        assert response.serial_number == b"99999T9999"
        assert response.exception > 0

    @pytest.mark.asyncio
    async def test_message_193_parsing(self):
        """Test exception response."""
        sample_193_response = bytes.fromhex(FUNCTION_193_MESSAGE)
        response = LxpResponse(sample_193_response)
        
        assert response.packet_error is False
        assert response.tcp_function == 193
        assert response.exception == 0
        assert response.dongle_serial == b"DG99999999"
        assert len(response.value)

