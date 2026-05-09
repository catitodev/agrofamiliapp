# Data module - CEPEA prices integration
import httpx
from typing import Dict, List, Optional


class CEPEAClient:
    BASE_URL = "https://www.cepea.esalq.usp.br/api"

    async def get_price(self, product: str) -> Optional[Dict]:
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                resp = await client.get(f"{self.BASE_URL}/product/{product}")
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass
        return None

    async def get_basket_price(self, basket: str = "familia") -> Optional[Dict]:
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                resp = await client.get(f"{self.BASE_URL}/cesta/{basket}")
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass
        return None

    def format_product_query(self, product_name: str) -> str:
        products = {
            "milho": "milho",
            "feijão": "feijao",
            "soja": "soja",
            "café": "cafe",
            "arroz": "arroz",
            "trigo": "trigo",
            "boi": "boi",
            "leite": "leite",
            "frango": "frango",
        }
        return products.get(product_name.lower(), product_name.lower())