import json

from data_sources.exchange_data.binance import fetch_latest_exchange_data
from data_sources.market_data.coingecko import fetch_latest_market_data
from data_sources.news.crypto_news import fetch_latest_crypto_news
from data_sources.social_media.reddit import fetch_posts


def create_latest_features():
    binance_dfs = {
        k: v.astype({"Timestamp": "str"}).to_dict("tight")
        for k, v in fetch_latest_exchange_data().items()
    }
    coingecko_market_data = fetch_latest_market_data()
    crypto_news_data = fetch_latest_crypto_news()[:5]  # hardcoded for demo
    reddit_posts = str(fetch_posts())
    return json.dumps(
        {
            "binance": binance_dfs,
            "coingecko": coingecko_market_data,
            "crypto-news": crypto_news_data,
            "reddit": reddit_posts,
        }
    )
