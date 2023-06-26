import os

import httpx


async def get_btc_usd_value() -> float:
    url = os.getenv('BTC_API_URL')
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return float(response.json().get('data').get('priceUsd'))
