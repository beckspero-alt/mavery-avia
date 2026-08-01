import os
import httpx
from dotenv import load_dotenv

load_dotenv()


class MaveryBackend:

    def __init__(self):

        self.base_url = os.getenv(
            "MAVERY_BACKEND",
            "http://127.0.0.1:8000"
        )

    async def get_live_vehicle(self):
        """
        Fetch live vehicle telemetry from
        the Mavery FetchAI endpoint.
        """

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.get(
                f"{self.base_url}/api/fetchai/live"
            )

        response.raise_for_status()

        return response.json()


mavery_backend = MaveryBackend()