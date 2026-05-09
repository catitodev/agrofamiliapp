# Data module - MAPA/SDA integration
import httpx
from typing import Dict, List


class MAPAClient:
    BASE_URL = "https://www.gov.br/agricultura"

    async def get_organic_certifiers(self) -> List[Dict]:
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                resp = await client.get(f"{self.BASE_URL}/pt-br/次/calendario")
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass
        return []

    async def get_sisorg_operators(self, state: str = None) -> List[Dict]:
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                resp = await client.get(
                    "https://www.gov.br/agricultura/pt-br/assuntos/sustentabilidade/organicos/organicos-e-agricultura-familiar/sisorg",
                    timeout=15
                )
                if resp.status_code == 200:
                    return {"status": "available"}
            except Exception:
                pass
        return {}