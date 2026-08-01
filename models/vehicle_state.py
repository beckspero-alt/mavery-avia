from dataclasses import dataclass
from typing import List


@dataclass
class VehicleState:
    """
    Live vehicle telemetry received from Jimi IoT.
    This becomes the 'brain input' for the Fetch.ai Vehicle Agent.
    """

    vehicle_id: str

    rpm: float

    speed: float

    battery_voltage: float

    coolant_temperature: float

    fuel_level: float

    engine_running: bool

    odometer: float

    fault_codes: List[str]

    timestamp: str