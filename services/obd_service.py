import requests

# Your existing Mavery FastAPI backend
API_BASE = "http://127.0.0.1:8000"


def get_live_vehicle_data(vehicle_id: str):
    """
    Fetch the latest live OBD data
    from the existing Mavery backend.
    """

    try:
        response = requests.get(
            f"{API_BASE}/api/vehicle/{vehicle_id}/live"
        )

        if response.status_code == 200:
            return response.json()

        return {
            "success": False,
            "error": f"Server returned {response.status_code}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }