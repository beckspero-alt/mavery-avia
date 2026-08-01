class AutonomousDecisionEngine:

    def decide(self, analysis):

        risk = analysis["risk_score"]

        confidence = 100

        if risk >= 80:

            return {
                "decision": "Emergency Intervention",
                "confidence": confidence,
                "priority": "Critical",
                "action": [
                    "Notify driver",
                    "Recommend stopping vehicle",
                    "Recommend towing",
                    "Recommend mechanic"
                ]
            }

        elif risk >= 50:

            return {
                "decision": "Schedule Maintenance",
                "confidence": confidence,
                "priority": "High",
                "action": [
                    "Notify driver",
                    "Recommend workshop inspection"
                ]
            }

        elif risk >= 20:

            return {
                "decision": "Continue Monitoring",
                "confidence": confidence,
                "priority": "Medium",
                "action": [
                    "Increase monitoring frequency"
                ]
            }

        return {
            "decision": "Vehicle Healthy",
            "confidence": confidence,
            "priority": "Normal",
            "action": [
                "Continue monitoring"
            ]
        }


decision_engine = AutonomousDecisionEngine()