# Data module - INMET weather API integration
import httpx
from typing import Dict, List, Optional


class INMETClient:
    BASE_URL = "https://apihm.inmet.gov.br"

    async def get_forecast(self, city_code: str) -> Dict:
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                resp = await client.get(f"{self.BASE_URL}/previsao/{city_code}")
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass
        return {}

    async def get_stations(self, state: str = None) -> List[Dict]:
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                url = f"{self.BASE_URL}/estacao"
                if state:
                    url += f"/{state}"
                resp = await client.get(url)
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass
        return []

    def get_city_code(self, city: str, state: str) -> Optional[str]:
        codes = {
            "petrolina": "2609907",
            "juazeiro": "2916808",
            "salvador": "2927409",
            "recife": "2611601",
            "fortaleza": "2307600",
            "belo horizonte": "3106208",
            "rio de janeiro": "3304557",
            "sao paulo": "3550308",
            "curitiba": "4106902",
            "florianopolis": "4205407",
            "porto alegre": "4314902",
            "goiania": "5208707",
            "campo grande": "5002704",
            "manaus": "1302603",
            "belem": "1501402",
            "aracaju": "2800308",
        }
        key = city.lower()
        return codes.get(key)