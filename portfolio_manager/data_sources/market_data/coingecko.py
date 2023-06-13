from typing import List
from datetime import datetime

from utils.dynaconf_utils import settings
from utils.httpx_utils import request

URL = settings.COINGECKO_API


def get_coins() -> List[dict]:
    """
    Get a list of coins asynchronously.

    Returns:
        List[dict]: A list of coins.
    """
    return request("GET", f"{URL}/coins/list")


def get_history_data(id: str, dt: datetime) -> dict:
    """
    Get historical data for a specific coin asynchronously.

    Args:
        id (str): The ID of the coin.
        dt (datetime): The date for the historical data.

    Returns:
        dict: The historical data for the specified coin and date.
    """
    params = {"date": dt.strftime("%d-%m-%Y")}
    return request("GET", f"{URL}/coins/{id}/history", params=params)


def fetch_market_data(dt: datetime):
    symbol_ids = None
    if settings.COINGECKO_SYMBOL_IDS:
        symbol_ids = settings.COINGECKO_SYMBOL_IDS
    else:
        coins = get_coins()
        symbol_ids = list(map(lambda x: x["id"], coins))

    results = {}
    for symbol_id in symbol_ids:
        data = get_history_data(symbol_id, dt)
        if not data:
            continue
        results.update(
            {
                symbol_id: {
                    "market_data": data.get("market_data"),
                    "community_data": data.get("community_data"),
                    "public_interest_stats": data.get("public_interest_stats"),
                }
            }
        )

    return results


def fetch_latest_market_data():
    return fetch_market_data(
        datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    )
