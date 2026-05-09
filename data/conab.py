# Data module - CONAB integration
import httpx
from typing import Dict, List


class CONABClient:
    BASE_URL = "https://portaldeinformacoes.conab.gov.br/api"

    async def get_prices(self, product: str = None, state: str = None) -> List[Dict]:
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                params = {}
                if product:
                    params["produto"] = product
                if state:
                    params["estado"] = state
                resp = await client.get(f"{self.BASE_URL}/precos", params=params)
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass
        return []

    async def get_paa_calls(self, state: str = None) -> List[Dict]:
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                params = {}
                if state:
                    params["estado"] = state
                resp = await client.get(f"{self.BASE_URL}/paa/chamadas", params=params)
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass
        return []