import httpx
import pytz
from datetime import datetime, timedelta
from typing import List

from utils.dynaconf_utils import settings
from utils.dt_utils import convert_to_utc
from utils.httpx_utils import request

URL = settings.CRYPTO_NEWS_API
API_KEY = settings.CRYPTO_NEWS_API_KEY

DT_FORMAT = "%a, %d %b %Y %H:%M:%S %z"
DT_TZ = "US/Eastern"


def get_crypto_news(symbols: List[str], start_dt: datetime, items: int = 50) -> dict:
    """
    Retrieve cryptocurrency news articles asynchronously.

    Args:
        symbols (List[str]): List of symbols to filter the news.
        start_dt (datetime): Start datetime to retrieve news from.
        items (int, optional): Number of news items to retrieve. Defaults to 50.

    Returns:
        dict: Dictionary containing the retrieved cryptocurrency news articles.
    """
    start_dt_utc = convert_to_utc(settings.TIME_ZONE, start_dt)

    total_pages = 9999
    params = {
        "tickers": ",".join(symbols),
        "token": API_KEY,
        "items": items,
    }

    json_results = []
    try:
        page_num = 1
        while page_num < total_pages:
            params.update({"page": page_num})
            json_result = request("GET", URL, params=params)
            json_results += json_result["data"]
            total_pages = json_result["total_pages"]
            if (
                convert_to_utc(
                    DT_TZ, datetime.strptime(json_results[-1]["date"], DT_FORMAT)
                )
                < start_dt_utc
            ) or (
                settings.CRYPTO_NEW_LIMIT_FOR_DEMO
                and len(json_results) >= settings.CRYPTO_NEW_LIMIT_FOR_DEMO
            ):
                break
            page_num += 1

    except httpx.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return json_results


def fetch_latest_crypto_news():
    symbols = settings.CRYPTO_NEWS_SYMBOLS

    latest_dt = datetime.today().replace(
        hour=0, minute=0, second=0, microsecond=0
    ) - timedelta(days=1)

    news_results = get_crypto_news(
        symbols,
        start_dt=latest_dt,
        items=3,
    )
    return [
        {
            "title": news["title"],
            "text": news["text"],
            "sentiment": news["sentiment"],
        }
        for news in news_results
    ]
