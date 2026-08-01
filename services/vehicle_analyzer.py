from models.vehicle_state import VehicleState


class VehicleAnalyzer:
    """
    MAVERY AVIA
    Autonomous Vehicle Intelligence Agent

    • Reads live telemetry
    • Predicts failures
    • Calculates repair urgency
    • Learns trends
    • Makes autonomous decisions
    """

    def analyze(self, vehicle: VehicleState):

        risk_score = 0

        findings = []

        urgency = "Low"

        # ==========================
        # Battery
        # ==========================

        if vehicle.battery_voltage is None:

            findings.append(
                "Battery voltage unavailable."
            )

        elif vehicle.battery_voltage < 11.8:

            risk_score += 25

            urgency = "Medium"

            findings.append(
                "Battery voltage critically low."
            )

        elif vehicle.battery_voltage >= 13.5:

            findings.append(
                "Battery charging normally."
            )

        else:

            findings.append(
                "Battery healthy."
            )

        # ==========================
        # Coolant
        # ==========================

        if vehicle.coolant_temperature is None:

            findings.append(
                "Coolant temperature unavailable (vehicle idle or ECU not reporting)."
            )

        elif vehicle.coolant_temperature > 110:

            risk_score += 45

            urgency = "Critical"

            findings.append(
                "Engine overheating."
            )

        elif vehicle.coolant_temperature > 100:

            risk_score += 25

            urgency = "High"

            findings.append(
                "Cooling system requires inspection."
            )

        else:

            findings.append(
                "Coolant temperature normal."
            )

        # ==========================
        # RPM
        # ==========================

        if vehicle.rpm is None:

            findings.append(
                "RPM unavailable (engine may be idling or ECU not reporting)."
            )

        elif vehicle.rpm > 4500:

            risk_score += 15

            findings.append(
                "Engine RPM unusually high."
            )

        else:

            findings.append(
                "Engine RPM normal."
            )

        # ==========================
        # Fuel
        # ==========================

        if vehicle.fuel_level is None:

            findings.append(
                "Fuel level unavailable."
            )

        elif vehicle.fuel_level < 10:

            risk_score += 10

            findings.append(
                "Fuel critically low."
            )

        else:

            findings.append(
                "Fuel level normal."
            )

        # ==========================
        # OBD Fault Codes
        # ==========================

        if vehicle.fault_codes:

            risk_score += 20

            findings.append(
                f"{len(vehicle.fault_codes)} OBD diagnostic fault code(s) detected."
            )

        # ==========================
        # HEALTH
        # ==========================

        health_score = max(0, 100 - risk_score)

        # ==========================
        # PREDICTION
        # ==========================

        if risk_score >= 70:

            prediction = "High probability of mechanical failure."

        elif risk_score >= 40:

            prediction = "Vehicle condition deteriorating."

        elif risk_score > 0:

            prediction = "Minor issues detected."

        else:

            prediction = "Vehicle connected. No critical issues detected."

        # ==========================
        # AUTONOMOUS DECISION ENGINE
        # ==========================

        if risk_score >= 70:

            autonomous_action = {

                "decision": "Schedule Emergency Maintenance",

                "priority": "Critical",

                "driver_notification": True,

                "mechanic_required": True,

                "continue_monitoring": True,

                "recommended_poll_interval": 10

            }

        elif risk_score >= 40:

            autonomous_action = {

                "decision": "Recommend Inspection",

                "priority": "High",

                "driver_notification": True,

                "mechanic_required": True,

                "continue_monitoring": True,

                "recommended_poll_interval": 20

            }

        elif risk_score > 0:

            autonomous_action = {

                "decision": "Monitor Vehicle",

                "priority": "Medium",

                "driver_notification": False,

                "mechanic_required": False,

                "continue_monitoring": True,

                "recommended_poll_interval": 30

            }

        else:

            autonomous_action = {

                "decision": "Vehicle Healthy",

                "priority": "Normal",

                "driver_notification": False,

                "mechanic_required": False,

                "continue_monitoring": True,

                "recommended_poll_interval": 60

            }

        return {

            "health_score": health_score,

            "risk_score": risk_score,

            "prediction": prediction,

            "urgency": urgency,

            "estimated_cost": self.estimate_cost(risk_score),

            "findings": findings,

            "autonomous_action": autonomous_action

        }

    def estimate_cost(self, risk_score):

        if risk_score >= 60:
            return "₦40,000 - ₦120,000"

        if risk_score >= 30:
            return "₦15,000 - ₦40,000"

        if risk_score > 0:
            return "₦5,000 - ₦15,000"

        return "₦0"


vehicle_analyzer = VehicleAnalyzer()