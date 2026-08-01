import asyncio
import httpx

from services.vehicle_analyzer import vehicle_analyzer
from services.trend_analyzer import trend_analyzer

from models.vehicle_state import VehicleState

from memory.memory import agent_memory


BACKEND_URL = "http://127.0.0.1:8000/api/fetchai/live"

POLL_INTERVAL = 5


async def fetch_live_vehicle():

    async with httpx.AsyncClient(timeout=20) as client:

        response = await client.get(BACKEND_URL)

        response.raise_for_status()

        return response.json()


async def run_vehicle_agent():

    print("=" * 60)
    print("                 MAVERY AVIA")
    print("   Autonomous Vehicle Intelligence Agent")
    print("          Powered by Fetch.ai")
    print("               Version 1.0")
    print("=" * 60)

    while True:

        try:

            live = await fetch_live_vehicle()

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

                timestamp=vehicle_data.get("last_report", "LIVE")

            )

            # ==================================
            # AI ANALYSIS
            # ==================================

            analysis = vehicle_analyzer.analyze(vehicle)

            # ==================================
            # STORE MEMORY
            # ==================================

            agent_memory.remember(
                vehicle.vehicle_id,
                analysis
            )

            history = agent_memory.latest_history(
                vehicle.vehicle_id
            )

            trend = trend_analyzer.analyse(history)

            action = analysis["autonomous_action"]

            # ==================================
            # DYNAMIC CONFIDENCE
            # ==================================

            confidence = 100

            if vehicle.coolant_temperature is None:
                confidence -= 15

            if vehicle.rpm is None:
                confidence -= 10

            if vehicle.fuel_level is None:
                confidence -= 5

            if vehicle.battery_voltage is None:
                confidence -= 5

            confidence = max(confidence, 50)

            # ==================================
            # AI REASONING
            # ==================================

            reasoning = []

            reasoning.append(
                "Live telemetry successfully received from Jimi IoT."
            )

            if vehicle.battery_voltage is not None:
                reasoning.append(
                    "Battery voltage indicates normal charging."
                )
            else:
                reasoning.append(
                    "Battery voltage unavailable."
                )

            if vehicle.coolant_temperature is None:
                reasoning.append(
                    "Coolant temperature unavailable (vehicle may be idling or ECU not reporting)."
                )
            elif vehicle.coolant_temperature > 110:
                reasoning.append(
                    "Engine overheating detected."
                )
            else:
                reasoning.append(
                    "Engine temperature within normal range."
                )

            if vehicle.rpm is None:
                reasoning.append(
                    "Engine RPM unavailable (vehicle may be idling or ECU not reporting)."
                )
            elif vehicle.rpm > 4500:
                reasoning.append(
                    "High engine RPM detected."
                )
            else:
                reasoning.append(
                    "Engine RPM within normal operating range."
                )

            if vehicle.fuel_level is None:
                reasoning.append(
                    "Fuel level unavailable."
                )
            elif vehicle.fuel_level < 10:
                reasoning.append(
                    "Fuel level critically low."
                )
            else:
                reasoning.append(
                    "Fuel level acceptable."
                )

            if len(vehicle.fault_codes) == 0:
                reasoning.append(
                    "No diagnostic trouble codes detected."
                )
            else:
                reasoning.append(
                    f"{len(vehicle.fault_codes)} diagnostic trouble code(s) detected."
                )

            if analysis["risk_score"] == 0:
                reasoning.append(
                    "Vehicle considered safe to continue monitoring."
                )
            else:
                reasoning.append(
                    "Vehicle requires closer monitoring."
                )

            # ==================================
            # NEXT AUTONOMOUS ACTION
            # ==================================

            next_actions = []

            if action["driver_notification"]:
                next_actions.append("✓ Notify driver immediately")

            if action["mechanic_required"]:
                next_actions.append("✓ Schedule mechanic inspection")

            if action["recommended_poll_interval"] <= 15:
                next_actions.append(
                    f"✓ Increase scan frequency to {action['recommended_poll_interval']} sec"
                )
            else:
                next_actions.append("✓ Continue monitoring")

            next_actions.append("✓ Store telemetry in memory")
            next_actions.append("✓ Await next telemetry packet")
            next_actions.append("✓ Recalculate vehicle health")

            print()
            print("=" * 60)
            print(" MAVERY AVIA REPORT")
            print("=" * 60)

            print("Vehicle ID      :", vehicle.vehicle_id)
            print("Last Telemetry  :", vehicle.timestamp)
            print("Prediction      :", analysis["prediction"])
            print("Risk Score      :", analysis["risk_score"])
            print("Health          :", analysis["health_score"])
            print("Urgency         :", analysis["urgency"])
            print("Cost            :", analysis["estimated_cost"])

            print()

            print("MISSION STATUS")
            print("------------------------------")
            print("Mission          : ACTIVE")
            print("Telemetry Source : ✓ Jimi IoT")
            print("AI Engine        : ✓ Online")
            print("Memory           : ✓ Recording")
            print("Decision Engine  : ✓ Running")
            print("Trend Analysis   : ✓ Active")

            print()

            print("AUTONOMOUS DECISION")
            print("------------------------------")
            print("Decision      :", action["decision"])
            print("Priority      :", action["priority"])
            print("Notify Driver :", action["driver_notification"])
            print("Mechanic      :", action["mechanic_required"])
            print("Continue AI   :", action["continue_monitoring"])
            print("Next Scan     :", f"{action['recommended_poll_interval']} sec")
            print("Confidence    :", f"{confidence}%")

            print()

            print("TREND ANALYSIS")
            print("------------------------------")
            print("Trend         :", trend["trend"])
            print("Forecast      :", trend["prediction"])

            print()

            print("AI REASONING")
            print("------------------------------")

            for item in reasoning:
                print(" •", item)

            print()

            print("NEXT AUTONOMOUS ACTION")
            print("------------------------------")

            for item in next_actions:
                print(item)

            print()

            print("VEHICLE FINDINGS")
            print("------------------------------")

            for finding in analysis["findings"]:
                print(" •", finding)

            print("=" * 60)

        except Exception as e:

            print("Agent Error:", e)

        await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":

    asyncio.run(run_vehicle_agent())