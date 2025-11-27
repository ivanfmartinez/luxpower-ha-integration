# my_modbus_bridge/classes/register_constants.py

# INPUT registers
REGISTER_BATTERY_VOLTAGE = 4
REGISTER_BATTERY_SOC_SOH = 5

#
# Luxpower Inverter Modbus RTU Protocol - Complete Hold Register Reference
#
# This file contains constants for ALL Hold Register addresses (7-241)
# based on the "06-01-01-PTC-Luxpower MODBUS Protocol_2024.04.26.pdf" document.
#
# No registers have been skipped.
#

# --- Firmware and Device Information (Read-Only) ---
H_FIRMWARE_CODE_0_1 = 7 # FWCode0, FWCode1. See "Software Version Definition file" for model and derived model codes.
H_FIRMWARE_CODE_2_3 = 8 # FWCode2, FWCode3. See "Software Version Definition file" for ODM and region codes.
H_SOFTWARE_VERSION_SLAVE_COM = 9 # Slave Ver (Redundant CPU) and Com Ver (Communication CPU).
H_SOFTWARE_VERSION_CNTL_FW = 10 # Cntl Ver (Control CPU) and FWVer (External FW).

# --- System Control & Time ---
H_RESET_SETTINGS = 11 # Register for system resets. Bit 7: 1 to restart inverter. Bits 8-15 are reserved.
H_TIME_YEAR_MONTH = 12 # Inverter time-year (Range: 17-255) and time-month (Range: 1-12).
H_TIME_DATE_HOUR = 13 # Inverter time-day (Range: 1-31) and time-hour (Range: 0-23).
H_TIME_MINUTE_SECOND = 14 # Inverter time-minute (Range: 0-59) and time-second (Range: 0-59).
H_COM_ADDRESS = 15 # MODBUS communication address (Range: 0-150).
H_LANGUAGE_AND_DEVICE_TYPE = 16 # Language (0: English, 1: German) and DTC (Device Type, 0-31).
# Register 17-18 are not defined in the Hold Register table.
H_DEVICE_TYPE_HIGH_SPEED = 19 # DTC:Device type. 3: XOLTA (for high-speed communication interval).
H_PV_INPUT_MODEL = 20 # Sets PV input configuration. 0:No PV, 1:PV1, 2:PV2, 3:PV1&2 parallel, 4:PV1&2 separate, etc.
H_FUNCTION_ENABLE_1 = 21
# Bit 0: EPSEn - Off-grid mode enable
# Bit 1: OVFLoadDerateEn - Overfrequency load reduction enable
# Bit 2: DRMSEN - DRMS enable
# Bit 3: LVRTEN - Low voltage ride-through enable
# Bit 4: AntilslandEn - Anti-islanding enable
# Bit 5: NeutralDetectEn - Neutral detection enable
# Bit 6: GridOnPowerSSEn - On-grid power soft start enable
# Bit 7: ACChargeEn - AC charging enable
# Bit 8: SWSeamlesslyEn - Seamless off-grid switching enable
# Bit 9: SetToStandby - 0: Standby, 1: Power on
# Bit 10: ForcedDischgEn - Forced discharge enable
# Bit 11: ForcedChgEn - Force charge enable
# Bit 12: ISOEn - ISO enable
# Bit 13: GFCIEn - GFCI enable
# Bit 14: DCIEN - DCI enable

# --- Grid & Power Settings ---
H_FUNCTION_ENABLE_2_AND_PV_START_VOLT = 22 # Combined register: Bit 15=FeedInGridEn, Bits 0-14=StartPVVolt (Unit: 0.1V, Range: 900-5000).
H_CONNECT_TIME = 23 # Waiting time of on-grid (Unit: s, Range: 30-600).
H_RECONNECT_TIME = 24 # Waiting time of Reconnect on-grid (Unit: s, Range: 0-900).
H_GRID_VOLT_CONN_LOW = 25 # The lower limit of the allowed on-grid voltage (Unit: 0.1V).
H_GRID_VOLT_CONN_HIGH = 26 # The upper limit of the allowed on-grid voltage (Unit: 0.1V).
H_GRID_FREQ_CONN_LOW = 27 # The lower limit of the allowed on-grid frequency (Unit: 0.01Hz).
H_GRID_FREQ_CONN_HIGH = 28 # The upper limit of the allowed on-grid frequency (Unit: 0.01Hz).
H_GRID_VOLT_LIMIT_1_LOW = 29 # Grid voltage level 1 undervoltage protection point (Unit: 0.1V).
H_GRID_VOLT_LIMIT_1_HIGH = 30 # Grid voltage level 1 overvoltage protection point (Unit: 0.1V).
H_GRID_VOLT_LIMIT_1_LOW_TIME = 31 # Grid voltage level 1 undervoltage protection time (Unit: Main period).
H_GRID_VOLT_LIMIT_1_HIGH_TIME = 32 # Grid voltage level 1 overvoltage protection time (Unit: Main period).
H_GRID_VOLT_LIMIT_2_LOW = 33 # Grid voltage level 2 undervoltage protection point (Unit: 0.1V).
H_GRID_VOLT_LIMIT_2_HIGH = 34 # Grid voltage level 2 overvoltage protection point (Unit: 0.1V).
H_GRID_VOLT_LIMIT_2_LOW_TIME = 35 # Grid voltage level 2 undervoltage protection time (Unit: Main period).
H_GRID_VOLT_LIMIT_2_HIGH_TIME = 36 # Grid voltage level 2 overvoltage protection time (Unit: Main period).
H_GRID_VOLT_LIMIT_3_LOW = 37 # Grid voltage level 3 undervoltage protection point (Unit: 0.1V).
H_GRID_VOLT_LIMIT_3_HIGH = 38 # Grid voltage level 3 overvoltage protection point (Unit: 0.1V).
H_GRID_VOLT_LIMIT_3_LOW_TIME = 39 # Grid voltage level 3 undervoltage protection time (Unit: Main period).
H_GRID_VOLT_LIMIT_3_HIGH_TIME = 40 # Grid voltage level 3 overvoltage protection time (Unit: Main period).
H_GRID_VOLT_MOV_AVG_HIGH = 41 # Grid voltage sliding average overvoltage protection point (Unit: 0.1V).
H_GRID_FREQ_LIMIT_1_LOW = 42 # Grid frequency level 1 underfrequency protection point (Unit: 0.01Hz).
H_GRID_FREQ_LIMIT_1_HIGH = 43 # Grid frequency level 1 overfrequency protection point (Unit: 0.01Hz).
H_GRID_FREQ_LIMIT_1_LOW_TIME = 44 # Grid frequency level 1 underfrequency protection time (Unit: Main period).
H_GRID_FREQ_LIMIT_1_HIGH_TIME = 45 # Grid frequency level 1 overfrequency protection time (Unit: Main period).
H_GRID_FREQ_LIMIT_2_LOW = 46 # Grid frequency level 2 underfrequency protection point (Unit: 0.01Hz).
H_GRID_FREQ_LIMIT_2_HIGH = 47 # Grid frequency level 2 overfrequency protection point (Unit: 0.01Hz).
H_GRID_FREQ_LIMIT_2_LOW_TIME = 48 # Grid frequency level 2 underfrequency protection time (Unit: Main period).
H_GRID_FREQ_LIMIT_2_HIGH_TIME = 49 # Grid frequency level 2 overfrequency protection time (Unit: Main period).
H_GRID_FREQ_LIMIT_3_LOW = 50 # Grid frequency level 3 underfrequency protection point (Unit: 0.01Hz).
H_GRID_FREQ_LIMIT_3_HIGH = 51 # Grid frequency level 3 overfrequency protection point (Unit: 0.01Hz).
H_GRID_FREQ_LIMIT_3_LOW_TIME = 52 # Grid frequency level 3 underfrequency protection time (Unit: Main period).
H_GRID_FREQ_LIMIT_3_HIGH_TIME = 53 # Grid frequency level 3 overfrequency protection time (Unit: Main period).

# --- Q(V) and P(V) Curve Settings ---
H_MAX_Q_PERCENT_FOR_QV = 54 # The maximum percentage of reactive power for the Q(V) curve (Unit: %).
H_QV_CURVE_V2L = 55 # Q(V) curve undervoltage 2 (Unit: 0.1V).
H_QV_CURVE_V1L = 56 # Q(V) curve undervoltage 1 (Unit: 0.1V).
H_QV_CURVE_V1H = 57 # Q(V) curve overvoltage 1 (Unit: 0.1V).
H_QV_CURVE_V2H = 58 # Q(V) curve overvoltage 2 (Unit: 0.1V).
H_REACTIVE_POWER_CMD_TYPE = 59 # 0:unit PF, 1:fixed PF, 2:default PF curve, 3:custom PF curve, 4:capacitive %, 5:inductive %, 6:QV curve, 7:QV_Dynamic.
H_ACTIVE_POWER_PERCENT_CMD = 60 # Active power percentage set value (Unit: %, Range: 0-100).
H_REACTIVE_POWER_PERCENT_CMD = 61 # Reactive power percentage set value (Unit: %, Range: 0-60).
H_PF_CMD = 62 # PF set value (Unit: 0.001).
H_POWER_SOFT_START_SLOPE = 63 # Loading rate, percentage of power increase per minute (Unit: %/min, Range: 1-4000).
H_LOCK_IN_GRID_V_FOR_PF_CURVE = 92 # cosphi(P) lock in voltage (Unit: 0.1V, Range: 2300-3000).
H_LOCK_OUT_GRID_V_FOR_PF_CURVE = 93 # cosphi(P) lock out voltage (Unit: 0.1V, Range: 1500-3000).
H_LOCK_IN_POWER_FOR_QV_CURVE = 94 # Q(V) lock in power (Unit: %, Range: 0-100).
H_LOCK_OUT_POWER_FOR_QV_CURVE = 95 # Q(V) lock out power (Unit: %, Range: 0-100).
H_DELAY_TIME_FOR_QV_CURVE = 96 # Q(V) delay (Unit: Main period, Range: 0-2000).

# --- Charging & Discharging Control ---
H_CHARGE_POWER_PERCENT_CMD_LEGACY = 64 # Charging power percentage setting (Legacy, see 138 for 0.1% precision).
H_DISCHG_POWER_PERCENT_CMD_LEGACY = 65 # Discharging power percentage setting (Legacy, see 139 for 0.1% precision).
H_AC_CHARGE_POWER_CMD = 66 # AC charge percentage setting (Unit: %, Range: 0-100).
H_AC_CHARGE_SOC_LIMIT = 67 # SOC limit setting for AC charging (Unit: %, Range: 0-100).
H_AC_CHARGE_START_TIME = 68 # AC charging start time (Hour and Minute).
H_AC_CHARGE_END_TIME = 69 # AC charging end time (Hour and Minute).
H_AC_CHARGE_START_TIME_1 = 70 # AC charging period 1 start time.
H_AC_CHARGE_END_TIME_1 = 71 # AC charging period 1 end time.
H_AC_CHARGE_START_TIME_2 = 72 # AC charging period 2 start time.
H_AC_CHARGE_END_TIME_2 = 73 # AC charging period 2 end time.
H_CHARGE_FIRST_POWER_CMD = 74 # Charging priority percentage setting (Unit: %, Range: 0-100).
H_CHARGE_FIRST_SOC_LIMIT_AND_START_TIME = 75 # Charging priority SOC limit setting and Start Hour.
H_CHARGE_FIRST_START_MINUTE = 76 # Charge priority start time minute.
H_CHARGE_FIRST_END_TIME = 77 # Charging priority end time (Hour and Minute).
H_CHARGE_FIRST_START_MINUTE_1 = 78 # Charging priority period 1 start time minute.
H_CHARGE_FIRST_END_TIME_1 = 79 # Charging priority period 1 end time.
H_CHARGE_FIRST_START_TIME_2 = 80 # Charging priority period 2 start time.
H_CHARGE_FIRST_END_TIME_2 = 81 # Charging priority period 2 end time.
H_FORCED_DISCHARGE_POWER_CMD = 82 # Forced discharge percentage setting (Unit: %, Range: 0-100).
H_FORCED_DISCHARGE_SOC_LIMIT_AND_START_TIME = 83 # Forced discharge SOC limit and Start Hour.
H_FORCED_DISCHARGE_START_TIME = 84 # Forced discharge start time.
H_FORCED_DISCHARGE_END_TIME = 85 # Forced discharge end time.
H_FORCED_DISCHARGE_START_TIME_1 = 86 # Forced discharge period 1 start time.
H_FORCED_DISCHARGE_END_TIME_1 = 87 # Forced discharge period 1 end time.
H_FORCED_DISCHARGE_START_TIME_2 = 88 # Forced discharge period 2 start time.
H_FORCED_DISCHARGE_END_TIME_2 = 89 # Forced discharge period 2 end time.
H_EPS_VOLTAGE_SET = 90 # Off-grid output voltage level setting (e.g., 230, 240V).
H_EPS_FREQ_SET = 91 # Off-grid output frequency system settings (50, 60Hz).
H_DELAY_TIME_FOR_OVER_F_DERATE = 97 # Overfrequency load reduction delay (Unit: Main period, Range: 0-1000).
# Register 98 is not defined in the Hold Register table.
H_LEAD_ACID_CHARGE_VOLT_REF = 99 # Lead-acid battery charging specified voltage (Unit: 0.1V, Range: 500-590).
H_LEAD_ACID_CUT_VOLT_FOR_DISCHG = 100 # Lead-acid battery discharge cut-off voltage (Unit: 0.1V, Range: 400-520).
H_CHARGE_CURRENT = 101 # Charging current (Unit: A, Range: 0-140).
H_DISCHARGE_CURRENT = 102 # Discharging current (Unit: A, Range: 0-140).
H_MAX_BACKFLOW_POWER = 103 # Feed-in grid power setting (Unit: %, Range: 0-100).
# Register 104 is not defined in the Hold Register table.
H_EOD_SOC = 105 # Cut SOC for discharging (End of Discharge) (Unit: %, Range: 10-90).
H_LEAD_ACID_TEMP_LOW_LIMIT_DISCHG = 106 # Lead-acid Temperature low limit for discharging (Unit: 0.1°C).
H_LEAD_ACID_TEMP_UPPER_LIMIT_DISCHG = 107 # Lead-acid Temperature high limit for discharging (Unit: 0.1°C).
H_LEAD_ACID_TEMP_LOW_LIMIT_CHG = 108 # Lead-acid Temperature low limit for charging (Unit: 0.1°C).
H_LEAD_ACID_TEMP_UPPER_LIMIT_CHG = 109 # Lead-acid Temperature high limit for charging (Unit: 0.1°C).
H_FUNCTION_ENABLE_3 = 110
# Bit 0: ubPVGridOffEn
# Bit 1: ubFastZeroExport
# Bit 2: ubMicroGridEn
# Bit 3: ubBatShared
# Bit 4: ubChgLastEn
# Bits 5-6: CTSampleRatio
# Bit 7: BuzzerEn
# Bits 8-9: PVCTSampleType
# Bit 10: TakeLoadTogether
# Bit 11: OnGridWorkingMode
# Bits 12-13: PVCTSampleRatio
# Bit 14: GreenModeEn
# Bit 15: EcoModeEn
# Register 111 is not defined in the Hold Register table.
H_SET_SYSTEM_TYPE = 112 # 0:single, 1:single-phase parallel(P), 2:single-phase parallel(S), 3:three-phase(M), 4:2*208(M).
H_SET_COMPOSED_PHASE = 113 # Write-only: Clear(0) or set R/S/T phase. Read-only: shows composed phases.
H_CLEAR_FUNCTION = 114 # Write-only: 1 to clear Parallel Alarm.
H_OVF_DERATE_START_POINT = 115 # Over-frequency load reduction start frequency point (Unit: 0.01Hz, Range: 5000-5200).
H_PTOUSER_START_DISCHG_THRESHOLD = 116 # Device starts discharging when Ptouser higher than this value (Unit: 1W, Default: 50W).
H_PTOUSER_START_CHG_THRESHOLD = 117 # Device starts charging when Ptouser less than this value (Unit: 1W, Default: -50W).
H_VBAT_START_DERATING = 118 # For lead-acid, decrease discharging power when voltage lower than this value (Unit: 0.1V).
H_WCT_POWER_OFFSET = 119 # External CT Power compensation. PtoUser direction is positive (Unit: 1W).
H_SYSTEM_ENABLE_2 = 120 # Contains multiple settings:
# Bit 0: HalfHourACChrStartEn
# Bits 1-3: ACChargeType (0:dis, 1:time, 2:volt, 3:soc...)
# Bits 4-5: DischgCtrlType (0:volt, 1:soc, 2:both)
# Bit 6: OnGridEODType (0:volt, 1:soc)
# Bit 7: GenChargeType (0:volt, 1:soc)
# Registers 121-123 are not defined in the Hold Register table.
H_OVF_DERATE_END_POINT = 124 # Overfrequency load reduction ends at this frequency point (Unit: 0.01Hz, Range: 5000-5200).
H_SOC_LOW_LIMIT_FOR_EPS_DISCHG = 125 # SOC low limit for EPS discharge (Unit: %, Range: 0-EOD).
H_OPTIMAL_CHG_DISCHG_0_3 = 126 # Time period marks for 00:00-03:30. 0:no op, 1:AC chg, 2:PV chg, 3:dischg.
H_OPTIMAL_CHG_DISCHG_4_7 = 127 # Time period marks for 04:00-07:30.
H_OPTIMAL_CHG_DISCHG_8_11 = 128 # Time period marks for 08:00-11:30.
H_OPTIMAL_CHG_DISCHG_12_15 = 129 # Time period marks for 12:00-15:30.
H_OPTIMAL_CHG_DISCHG_16_19 = 130 # Time period marks for 16:00-19:30.
H_OPTIMAL_CHG_DISCHG_20_23 = 131 # Time period marks for 20:00-23:30.
H_BAT_CELL_VOLT_LIMITS = 132 # Lower and Upper battery cell voltage limits (Unit: 0.1V).
H_BAT_CELL_NUMBERS = 133 # Number of battery cells in series and parallel.
H_UVF_DERATE_START_POINT = 134 # Underfrequency load reduction starting point (Unit: 0.01Hz, Range: 4500-5000).
H_UVF_DERATE_END_POINT = 135 # Underfrequency load reduction end point (Unit: 0.01Hz, Range: 4500-5000).
H_OVF_DERATE_RATIO = 136 # Underfrequency load ramp rate (Unit: %Pm/Hz, Range: 1-100).
H_SPEC_LOAD_COMPENSATE = 137 # The maximum amount of compensation for a specific load (Unit: W).
H_CHARGE_POWER_PERCENT_CMD = 138 # Charging power percentage setting (Unit: 0.1%, Range: 0-1000).
H_DISCHG_POWER_PERCENT_CMD = 139 # Discharging power percentage setting (Unit: 0.1%, Range: 0-1000).
H_AC_CHG_POWER_CMD_PRECISE = 140 # AC charge percentage setting (Unit: 0.1%, Range: 0-1000).
H_CHG_FIRST_POWER_CMD_PRECISE = 141 # Charging priority percentage setting (Unit: 0.1%, Range: 0-1000).
H_FORCED_DISCHG_POWER_CMD_PRECISE = 142 # Forced discharge percentage setting (Unit: 0.1%, Range: 0-1000).
H_ACTIVE_POWER_PERCENT_CMD_PRECISE = 143 # Inverse active percentage setting (Unit: 0.1%, Range: 0-1000).
H_FLOAT_CHARGE_VOLT = 144 # Float charge voltage (Unit: 0.1V, Range: 500-560).
H_OUTPUT_PRIORITY_CONFIG = 145 # 0:bat first, 1:PV first, 2:AC first.
H_LINE_MODE = 146 # 0:APL, 1:UPS, 2:GEN.
H_BATTERY_CAPACITY = 147 # Battery capacity for unmatched batteries (Unit: Ah, Range: 0-10000).
H_BATTERY_NOMINAL_VOLTAGE = 148 # Battery rating voltage for unmatched batteries (Unit: 0.1V, Range: 400-590).
H_EQUALIZATION_VOLT = 149 # Battery equalization voltage (Range: 500-590).
H_EQUALIZATION_INTERVAL = 150 # Balancing interval (Unit: Day, Range: 0-365).
H_EQUALIZATION_TIME = 151 # Balancing duration (Unit: hour, Range: 0-24).
H_AC_FIRST_START_TIME = 152 # AC load start time (Hour and Minute).
H_AC_FIRST_END_TIME = 153 # AC load end time (Hour and Minute).
H_AC_FIRST_START_TIME_1 = 154 # AC load period 1 start time.
H_AC_FIRST_END_TIME_1 = 155 # AC load period 1 end time.
H_AC_FIRST_START_TIME_2 = 156 # AC load period 2 start time.
H_AC_FIRST_END_TIME_2 = 157 # AC load period 2 end time.
H_AC_CHARGE_START_VOLT = 158 # Battery voltage of AC charging start (Unit: 0.1V, Range: 385-520).
H_AC_CHARGE_END_VOLT = 159 # Battery voltage of AC charging cut-off (Unit: 0.1V, Range: 480-590).
H_AC_CHARGE_START_SOC = 160 # SOC of AC charging start (Unit: %, Range: 0-90).
H_AC_CHARGE_END_SOC = 161 # SOC of AC charging end (Unit: %, Range: 0-90).
H_BAT_LOW_VOLTAGE_ALARM = 162 # Battery under-voltage alarm point (Unit: 0.1V, Range: 400-500).
H_BAT_LOW_BACK_VOLTAGE = 163 # Battery under-voltage alarm recovery point (Unit: 0.1V, Range: 420-520).
H_BAT_LOW_SOC_ALARM = 164 # Battery under-voltage alarm point (Unit: %, Range: 0-90).
H_BAT_LOW_BACK_SOC = 165 # Battery under-voltage alarm recovery point (Unit: %, Range: 20-100).
H_BAT_LOW_TO_UTILITY_VOLTAGE = 166 # Voltage point for battery undervoltage to grid transfer (Unit: 0.1V, Range: 444-514).
H_BAT_LOW_TO_UTILITY_SOC = 167 # SOC for battery undervoltage to grid transfer (Unit: %, Range: 0-100).
H_AC_CHARGE_BAT_CURRENT = 168 # Charge Current from AC (Unit: A, Range: 0-140).
H_ONGRID_EOD_VOLTAGE = 169 # On-grid end of discharge voltage (Unit: 0.1V, Range: 400-560).
# Register 170 is not defined in the Hold Register table.
H_SOCCURVE_BATVOLT1 = 171 # Voltage point 1 for SOC calibration (Unit: 0.1V, Range: 400-600).
H_SOCCURVE_BATVOLT2 = 172 # Voltage point 2 for SOC calibration (Unit: 0.1V, Range: 400-600).
H_SOCCURVE_SOC1 = 173 # SOC reading based on Voltage point 1 (Unit: 1%, Range: 0-100).
H_SOCCURVE_SOC2 = 174 # SOC reading based on Voltage point 2 (Unit: 1%, Range: 0-100).
H_SOCCURVE_INNER_RESISTANCE = 175 # Inner resistance of the battery (Unit: uOhm, Range: 0-100).
H_MAX_GRID_INPUT_POWER = 176 # Max. Grid import power limitation (Unit: 0.1kW).
H_GEN_RATED_POWER = 177 # The rated power of generator input (Unit: W).
# Register 178 is not defined in the Hold Register table.
H_FUNCTION_ENABLE_4 = 179 # uFunctionEn2 bits:
# Bit 0: uFunctionEn2.ACCTDirection (0=Normal, 1=Reversed)
# Bit 1: uFunctionEn2.PVCTDirection (0=Normal, 1=Reversed)
# Bit 2: uFunctionEn2.AFCIAlarmClr (0=null, 1=clear)
# Bit 3: uFunctionEn2.BatWakeupEn-PVSellFirst (0=Disable, 1=Enable)
# Bit 4: uFunctionEn2.VoltWattEn (0=Disable, 1=Enable)
# Bit 5: uFunctionEn2.TriptimeUnit (0=Disable, 1=Enable)
# Bit 6: uFunctionEn2.ActPowerCMDEn (0=Disable, 1=Enable)
# Bit 7: uFunctionEn2.ubGridPeakShaving (0=Disable, 1=Enable)
# Bit 8: uFunctionEn2.ubGenPeakShaving (0=Disable, 1=Enable)
# Bit 9: uFunctionEn2.ubBatChgControl (0=SOC, 1=Volt)
# Bit 10: uFunctionEn2.ubBatDischgControl (0=SOC, 1=Volt)
# Bit 11: uFunctionEn2.ubACcoupling (0=Disable, 1=Enable)
# Bit 12: uFunctionEn2.ubPVArcEn (0=Disable, 1=Enable)
# Bit 13: uFunctionEn2.ubSmartLoadEn (0=Generator, 1=Smart Load)
# Bit 14: uFunctionEn2.ubRSDDisable (0=Enable, 1=Disable)
# Bit 15: uFunctionEn2.OnGridAlwaysOn (0=Disable, 1=Enable)
H_AFCI_ARC_THRESHOLD = 180 # AFCI Arc Threshold (Unit: A, Range: 0-65535).
H_VOLTWATT_V1 = 181 # VoltWatt V1 (Unit: 0.1V). Default 1.06Vn.
H_VOLTWATT_V2 = 182 # VoltWatt V2 (Unit: 0.1V). Default 1.1Vn.
H_VOLTWATT_DELAYTIME = 183 # VoltWatt Delay Time (Unit: Main cnt, Range: 500-60000ms).
H_VOLTWATT_P2 = 184 # VoltWatt P2 (Unit: %).
H_VREF_QV = 185 # Vref for QV curve (Unit: 0.1V).
H_VREF_FILTERTIME = 186 # Vref filter time (Unit: s).
H_Q3_QV = 187 # Q3 for QV curve (Unit: %).
H_Q4_QV = 188 # Q4 for QV curve (Unit: %).
H_P1_QP = 189 # P1 for QP curve (Unit: %).
H_P2_QP = 190 # P2 for QP curve (Unit: %).
H_P3_QP = 191 # P3 for QP curve (Unit: %).
H_P4_QP = 192 # P4 for QP curve (Unit: %).
H_UVF_INCREASE_RATIO = 193 # Underfrequency load ramp rate (Unit: %Pm/Hz, Range: 1-100).
H_GEN_CHARGE_START_VOLT = 194 # Initial voltage for generator charging (Unit: 0.1V, Range: 384-520).
H_GEN_CHARGE_END_VOLT = 195 # Battery voltage at the end of generator charging (Unit: 0.1V, Range: 480-590).
H_GEN_CHARGE_START_SOC = 196 # SOC limit for generator charging (Unit: %, Range: 0-90).
H_GEN_CHARGE_END_SOC = 197 # SOC limit to end generator charging (Unit: %, Range: 20-100).
H_MAX_GEN_CHARGE_BAT_CURRENT = 198 # Max. Charge current from generator (Unit: A, Range: 0-4000).
H_OVER_TEMP_DERATE_POINT = 199 # Overtemperature load reduction point (Unit: 0.1°C, Range: 600-900).
# Register 200 is not defined in the Hold Register table.
H_CHARGE_FIRST_END_VOLT = 201 # Charging priority voltage limit (Unit: 0.1V, Range: 480-590).
H_FORCED_DISCHG_END_VOLT = 202 # Forced discharge voltage limit (Unit: 0.1V, Range: 400-560).
H_GRID_REGULATION = 203 # Grid regulation settings (Unit: bitfield, Range: 0-65535).
H_LEAD_CAPACITY = 204 # Capacity of the lead acid battery (Unit: Ah, Range: 50-5000).
H_GRID_TYPE = 205 # 0:Split240V, 1:3ph-208V, 2:Single-240V, 3:Single-230V, 4:Split-200V.
H_GRID_PEAK_SHAVING_POWER = 206 # Grid Peak Shaving Power (Unit: 0.1kW, Range: 0-255).
H_GRID_PEAK_SHAVING_SOC = 207 # Grid Peak Shaving SOC (Unit: %, Range: 0-100).
H_GRID_PEAK_SHAVING_VOLT = 208 # Grid Peak Shaving Voltage (Unit: 0.1V, Range: 480-590).
H_PEAK_SHAVING_START_TIME = 209 # PeakShaving start time (Hour and Minute).
H_PEAK_SHAVING_END_TIME = 210 # PeakShaving end time (Hour and Minute).
H_PEAK_SHAVING_START_TIME_1 = 211 # PeakShaving period 1 start time.
H_PEAK_SHAVING_END_TIME_1 = 212 # PeakShaving period 1 end time.
H_SMART_LOAD_ON_VOLT = 213 # Smart Load On Voltage (Unit: 0.1V, Range: 480-590).
H_SMART_LOAD_OFF_VOLT = 214 # Smart Load Off Voltage (Unit: 0.1V, Range: 400-520).
H_SMART_LOAD_ON_SOC = 215 # Smart Load On SOC (Unit: %, Range: 0-100).
H_SMART_LOAD_OFF_SOC = 216 # Smart Load Off SOC (Unit: %, Range: 0-100).
H_START_PV_POWER = 217 # Start PV power (Unit: 0.1kW, Range: 0-120).
H_GRID_PEAK_SHAVING_SOC1 = 218 # Grid Peak Shaving SOC 1 (Unit: %, Range: 0-100).
H_GRID_PEAK_SHAVING_VOLT1 = 219 # Grid Peak Shaving Volt 1 (Unit: 0.1V, Range: 480-590).
H_AC_COUPLE_START_SOC = 220 # AC Couple Start SOC (Unit: %, Range: 0-100).
H_AC_COUPLE_END_SOC = 221 # AC Couple End SOC (Unit: %, Range: 0-255).
H_AC_COUPLE_START_VOLT = 222 # AC Couple Start Volt (Unit: 0.1V, Range: 400-595).
H_AC_COUPLE_END_VOLT = 223 # AC Couple End Volt (Unit: 0.1V, Range: 420-800).
H_LCD_CONFIG = 224 # Contains LCD Version, Screen Type, ODM, and Machine Model Code.
H_LCD_PASSWORD = 225 # Password for LCD Advanced page (Range: 0-65535).
# Register 226 is not defined in the Hold Register table.
H_BAT_STOP_CHARGE_SOC = 227 # SOC to stop charging battery (Unit: %, Range: 10-101).
H_BAT_STOP_CHARGE_VOLT = 228 # Voltage to stop charging battery (Unit: 0.1V, Range: 400-595).
# Register 229 is not defined in the Hold Register table.
H_METER_CONFIG = 230 # Contains MetersNum, MeasureType, InstallPhase.
H_RESET_RECORD = 231 # Bit 0: 1 to Reset the G100 lockout state.
H_GRID_PEAK_SHAVING_POWER_1 = 232 # GridPeakShavingPower1 (Unit: W, Range: 0-65535).
H_FUNCTION_ENABLE_5 = 233 # Function Enable bits:
# Bit 0: uFunction4En.ubQuickChgStartEn
# Bit 1: uFunction4En.ubBattBackupEn
# Bit 2: uFunction4En.ubMaintenanceEn
# Bit 3: uFunction4En.ubWorkingMode (7-day period work mode 1 or 2)
# Bit 4-7: uFunction4En.ubDryContactorMultiplex
# Bit 8-9: uFunction4En.ubExCTPosition (0=GridtoUser, 1=InvGridPort)
# Bit 10: uFunction4En.ubOverFreq_fstop (0=deactivated, 1=activated)
H_QUICK_CHG_TIME = 234 # Quick Charge Time (Unit: min, Range: 0-1440).

# The Calibration information only came when Battery Callibration is enabled
# But Luxpower support informed that even installer does not have access to enable this setting and not available on documentation
#  normally disabled because will get power from grid
H_NO_FULL_CHG_DAY_CONFIG = 235 # Read-only days counter (bits 0-7) and Calibration period setting (bits 8-15).

H_FLOAT_CHG_THRESHOLD = 236 # When charge current in CV lower than this, switch to float charge (Unit: 0.01C, Range: 1-255).
H_GEN_COOL_DOWN_TIME = 237 # Gen cool down time when dry contactor is off (Unit: 0.1min, Range: 1-255).
# Registers 238-240 are not defined in the Hold Register table.
H_PERMIT_SERVICE = 241 # Service mode enable (0=disable, non-0=enable, Range: 0-65535).

# --- Added in V23 (2025-06-14) ---

# WattNode Meter Settings
H_WATTNODE_CT_AMPS_1 = 248 # WattNode CT Amps Phase 1 (Unit: A, Range: 0-65535).
H_WATTNODE_CT_AMPS_2 = 249 # WattNode CT Amps Phase 2 (Unit: A, Range: 0-65535).
H_WATTNODE_CT_AMPS_3 = 250 # WattNode CT Amps Phase 3 (Unit: A, Range: 0-65535).
H_WATTNODE_CT_DIRECTIONS = 251 # WattNode CT Direction settings (Unit: bitfield, Range: 0-65535).

# Advanced Limits & Hysteresis
H_NEC_120_BUS_BAR_LIMIT = 252 # NEC 120% Bus Bar Limit (Unit: W, Range: 0-65535).
H_DELTA_SOC = 253 # SOC delta/hysteresis setting (Unit: %, Range: 0-100).
H_DELTA_VOLT = 254 # Voltage delta/hysteresis setting (Unit: 0.1V, Range: 0-100).
# Register 255 is not defined in the Hold Register table.

# Generator Time Scheduling
H_GEN_START_TIME = 256 # Generator start time (Hour and Minute).
H_GEN_END_TIME = 257 # Generator end time (Hour and Minute).
H_GEN_START_TIME_1 = 258 # Generator period 1 start time (Hour and Minute).
H_GEN_END_TIME_1 = 259 # Generator period 1 end time (Hour and Minute).
H_BUS_VOLT_HIGH_SET = 260 # Bus voltage high limit setting (Unit: 0.1V, Range: 0-8000).
H_DISCHARGE_RECOVERY = 261 # Discharge recovery setting (Unit: %, Range: 0-100).
H_GEN_END_TIME = 257 # Generator end time (Hour and Minute).
H_GEN_START_TIME_1 = 258 # Generator period 1 start time (Hour and Minute).
H_GEN_END_TIME_1 = 259 # Generator period 1 end time (Hour and Minute).