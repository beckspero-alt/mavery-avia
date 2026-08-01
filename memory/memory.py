from datetime import datetime


class AgentMemory:

    def __init__(self):
        self.history = []

    # ==========================================
    # Store analysis
    # ==========================================
    def remember(self, vehicle_id: str, analysis: dict):

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "vehicle_id": vehicle_id,
            "analysis": analysis,
        }

        self.history.append(record)

        # Keep only latest 1000 analyses
        if len(self.history) > 1000:
            self.history.pop(0)

        return record

    # ==========================================
    # Latest record
    # ==========================================
    def latest(self, vehicle_id: str):

        for item in reversed(self.history):

            if item["vehicle_id"] == vehicle_id:
                return item

        return None

    # ==========================================
    # Latest history (used by Trend Analyzer)
    # ==========================================
    def latest_history(self, vehicle_id: str, limit: int = 5):

        records = []

        for item in reversed(self.history):

            if item["vehicle_id"] == vehicle_id:
                records.append(item)

            if len(records) >= limit:
                break

        records.reverse()

        return records

    # ==========================================
    # Entire memory
    # ==========================================
    def all(self):

        return self.history


agent_memory = AgentMemory()