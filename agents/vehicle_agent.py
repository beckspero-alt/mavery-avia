from uagents import Agent, Context

from services.mavery_backend import mavery_backend
from services.vehicle_analyzer import vehicle_analyzer
from models.vehicle_state import VehicleState


agent = Agent(
    name="mavery_vehicle_agent",
    seed="mavery_fetch_ai_vehicle_agent",
)


@agent.on_interval(period=15)
async def monitor_vehicle(ctx: Context):

    ctx.logger.info("Checking live vehicle telemetry...")

    try:

        live = await mavery_backend.get_vehicle_health()

        vehicle_data = live.get("vehicle", {})
        raw = live.get("raw_obd", {})

        battery = vehicle_data.get("battery_voltage")

        if battery is not None:
            battery = float(battery) / 1000

        rpm = vehicle_data.get("rpm")

        if rpm is not None:
            rpm = float(rpm)

        speed = vehicle_data.get("speed")

        if speed is not None:
            speed = float(speed)

        coolant = vehicle_data.get("coolant_temperature")

        if coolant is not None:
            coolant = float(coolant)

        fuel = vehicle_data.get("fuel_remaining")

        if fuel is not None:
            fuel = float(fuel)

        vehicle = VehicleState(

            vehicle_id=raw.get("imei", "LIVE"),

            rpm=rpm,

            speed=speed,

            battery_voltage=battery,

            coolant_temperature=coolant,

            fuel_level=fuel,

            engine_running=vehicle_data.get("engine_running"),

            odometer=vehicle_data.get("odometer"),

            fault_codes=[],

            timestamp=vehicle_data.get("last_report", "LIVE"),

        )

        result = vehicle_analyzer.analyze(vehicle)

        ctx.logger.info("=" * 50)
        ctx.logger.info("MAVERY AVIA Decision")
        ctx.logger.info(result)
        ctx.logger.info("=" * 50)

    except Exception as e:

        ctx.logger.exception(e)


if __name__ == "__main__":

    print("=" * 50)
    print("MAVERY AVIA Vehicle Agent Started")
    print("=" * 50)

    agent.run()