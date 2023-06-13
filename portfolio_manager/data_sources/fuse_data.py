import json

from data_sources.exchange_data.binance import fetch_latest_exchange_data
from data_sources.market_data.coingecko import fetch_latest_market_data
from data_sources.news.crypto_news import fetch_latest_crypto_news
from data_sources.social_media.reddit import fetch_posts
from utils.dynaconf_utils import settings


def create_latest_features():
    binance_dfs = {
        k: v.astype({"Timestamp": "str"}).to_csv()
        for k, v in fetch_latest_exchange_data().items()
    }
    coingecko_market_data = fetch_latest_market_data()
    crypto_news_data = fetch_latest_crypto_news()
    try:
        reddit_posts = fetch_posts()
    except Exception as e:
        print(e)
        raise e
    return json.dumps(
        {
            # "binance": binance_dfs,
            "coingecko": coingecko_market_data,
            "crypto-news": crypto_news_data,
            "reddit": reddit_posts,
        }
    )
