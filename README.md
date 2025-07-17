# LuxPower Modbus Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/ant0nkr/luxpower-modbus-hacs?style=for-the-badge)](https://github.com/ant0nkr/luxpower-modbus-hacs/releases)
[![GitHub License](https://img.shields.io/github/license/ant0nkr/luxpower-modbus-hacs?style=for-the-badge)](https://github.com/ant0nkr/luxpower-modbus-hacs/blob/main/LICENSE)

A comprehensive Home Assistant integration to monitor and control LuxPower inverters via their Modbus TCP interface.

This integration connects directly to your inverter's WiFi dongle, providing real-time data and control over various settings without relying on the cloud.

## Features

* **Real-time Monitoring:** Track PV power, battery state of charge (SOC), grid import/export, load consumption, and more.
* **Inverter Control:** Change charge/discharge currents, set timed charging/discharging periods, and enable/disable features like grid feed-in.
* **Detailed States:** A user-friendly text sensor shows exactly what the inverter is doing (e.g., "PV Powering Load & Charging Battery").
* **Calculated Sensors:** Includes derived sensors like "Load Percentage" for a clearer view of your system's performance.
* **Local Polling:** All communication is local. No cloud dependency.

## Installation

### Prerequisites

Your LuxPower inverter's WiFi data logging dongle must be connected to the same local network as your Home Assistant instance. You will need to know its IP address.

### HACS (Recommended)

This integration is available in the default HACS repository.
1.  Go to **HACS** > **Integrations**.
2.  Click the **Explore & Download Repositories** button.
3.  Search for "LuxPower Modbus" and add it.
4.  Restart Home Assistant as prompted.

### Manual Installation

1.  Copy the `lxp_modbus` folder from this repository into your Home Assistant `custom_components` directory.
2.  Restart Home Assistant.

## Configuration

Configuration is done entirely through the Home Assistant UI.

1.  Go to **Settings** > **Devices & Services**.
2.  Click **Add Integration** and search for **"Luxpower Inverter Setup"**.
3.  Fill in the required details for your inverter.

### Configuration Options

| Name                      | Type   | Description                                                                                 |
| ------------------------- | ------ | ------------------------------------------------------------------------------------------- |
| **IP Address** | string | **(Required)** The IP address of your inverter's WiFi dongle.                                 |
| **Port** | integer| **(Required)** The communication port for the Modbus connection, typically `8000`.              |
| **Dongle Serial Number** | string | **(Required)** The 10-character serial number of your WiFi dongle.                            |
| **Inverter Serial Number**| string | **(Required)** The 10-character serial number of your inverter.                               |
| **Polling Interval** | integer| **(Required)** How often (in seconds) to poll the inverter for data. Default is 10.           |
| **Inverter Rated Power** | integer| **(Required)** The rated power of your inverter in Watts (e.g., `5000` for a 5kW model).      |
| **Entity Prefix** | string | (Optional) A custom prefix for all entity names (e.g., 'LXP'). Leave blank for no prefix.   |

## Entities

This integration creates a wide range of entities to give you full visibility and control over your inverter.

#### Sensors
Provides detailed operational data, including:
* Inverter State (Text and Code)
* Battery SOC & SOH
* PV Power (Total and per-string)
* Grid Import/Export Power
* Load Power
* Battery Charge/Discharge Power
* Daily & Total Energy Statistics (PV, Grid, Load, etc.)
* Temperatures (Battery, Radiator, etc.)
* Voltages, Currents, and Frequencies for Grid, EPS, and Battery.
* Calculated Load Percentage

#### Numbers
Allows control over inverter settings:
* Charge & Discharge Currents
* AC Charge Power Limit
* End of Discharge (EOD) SOC
* Battery Stop Charging Voltage/SOC

#### Switches
Enable or disable key features on the fly:
* AC Charging Enable
* Feed-In Grid Enable
* Forced Discharge Enable
* Eco & Green Modes

#### Selects
Choose from predefined operational modes:
* AC Charge Type (by Time, SOC, etc.)
* Output Priority (Battery first, PV first, etc.)

#### Time
Set schedules for timed operations:
* AC Charging Start & End Times
* Peak Shaving Start & End Times

## Debugging

If you are having issues, you can enable debug logging by adding the following to your `configuration.yaml` file:

```yaml
logger:
  default: info
  logs:
    custom_components.lxp_modbus: debug
