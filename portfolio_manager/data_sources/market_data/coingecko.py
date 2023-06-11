from typing import List
from datetime import datetime

from utils.dynaconf_utils import settings
from utils.httpx_utils import request

URL = settings.COINGECKO_API


def get_coins() -> List[dict]:
    """
    Get a list of coins.

    Returns:
        List[dict]: A list of coins.
    """
    return request("GET", f"{URL}/coins/list")


def get_history_data(id: str, dt: datetime) -> dict:
    """
    Get historical data for a specific coin.

    Args:
        id (str): The ID of the coin.
        dt (datetime): The date for the historical data.

    Returns:
        dict: The historical data for the specified coin and date.
    """
    params = {"date": dt.strftime("%d-%m-%Y")}
    return request("GET", f"{URL}/coins/{id}/history", params=params)
