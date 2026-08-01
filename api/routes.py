from fastapi import APIRouter
from pydantic import BaseModel

from agents.vehicle_health_agent import vehicle_health_agent
from memory.memory import agent_memory

router = APIRouter()


class VehicleTelemetry(BaseModel):

    vehicle_id: str

    battery_voltage: float | None = None
    coolant_temperature: float | None = None
    rpm: int | None = None
    speed: int | None = None
    fuel_remaining: float | None = None

    obd: dict = {}


@router.post("/vehicle/analyze")
async def analyze_vehicle(data: VehicleTelemetry):

    payload = data.model_dump()

    result = await vehicle_health_agent.analyze(payload)

    agent_memory.remember(
        data.vehicle_id,
        result
    )

    return result


@router.get("/vehicle/{vehicle_id}/latest")
async def latest(vehicle_id: str):

    result = agent_memory.latest(vehicle_id)

    if result is None:

        return {
            "message": "No memory found."
        }

    return result


@router.get("/memory")
async def memory():

    return agent_memory.all()