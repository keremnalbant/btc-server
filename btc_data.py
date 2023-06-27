import asyncio
import os

import httpx

url = os.getenv('BTC_API_URL')


async def get_btc_usd_value(retries=10) -> float:
    async with httpx.AsyncClient() as client:
        for _ in range(retries):
            try:
                response = await client.get(url)
                data = response.json().get('data')
                price_usd = float(data.get('priceUsd'))
                return price_usd
            except (httpx.HTTPError, ValueError, TypeError) as e:
                print(f"Error occurred: {e}")
                await asyncio.sleep(5)

    raise RuntimeError(f"Failed to get BTC USD value after {retries} retries.")
