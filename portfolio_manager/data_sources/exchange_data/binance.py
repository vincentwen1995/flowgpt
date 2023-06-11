from datetime import datetime
from typing import List

import ccxt
from utils.dynaconf_utils import settings

binance = ccxt.binance()
remove_list = set(settings.UNWANTED_SYMBOLS)


def load_symbols() -> List[str]:
    """
    Load symbols from the exchange.

    Returns:
        List[str]: A list of symbols.
    """
    exchange_info = binance.fapiPublicGetExchangeInfo()
    symbol_list = list(
        filter(
            lambda x: bool(x),
            [
                symbol["symbol"]
                if symbol["contractType"] == "PERPETUAL"
                and symbol["symbol"] not in remove_list
                and symbol["symbol"].endswith("USDT")
                else None
                for symbol in exchange_info["symbols"]
            ],
        )
    )
    return symbol_list


def extract_columns(data: List[dict], column_names: List[str]) -> List[dict]:
    """
    Extract specific columns from the data.

    Args:
        data (List[dict]): The input data.
        column_names (List[str]): The list of column names to extract.

    Returns:
        List[dict]: The extracted data with the specified columns.
    """
    return [{col: line[i] for i, col in enumerate(column_names)} for line in data]


def get_klines(
    exchange,
    symbol: str,
    start_time: datetime,
    interval: str = "1h",
    limit: int = 500,
) -> List[dict]:
    """
    Get Klines (candlestick) data for a specific symbol.

    Args:
        exchange: The exchange instance.
        symbol (str): The symbol to retrieve the data for.
        start_time (datetime): The start time of the data.
        interval (str, optional): The interval of the data (default: "1h").
        limit (int, optional): The number of data points to retrieve (default: 500).

    Returns:
        List[dict]: The Klines data for the specified symbol.
    """
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": str(exchange.parse8601(start_time)),
        "limit": limit,
    }
    data = exchange.fapiPublicGetKlines(params=params)
    columns = [
        "MTS",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "closeMTS",
        "quote_volume",
        "trade_num",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
    ]
    return extract_columns(data, columns)


def get_funding_rate(
    exchange, symbol: str, start_time: datetime, limit: int = 500
) -> List[dict]:
    """
    Get funding rates for a specific symbol.

    Args:
        exchange: The exchange instance.
        symbol (str): The symbol to retrieve the funding rates for.
        start_time (datetime): The start time of the funding rates.
        limit (int, optional): The number of funding rates to retrieve (default: 500).

    Returns:
        List[dict]: The funding rates data for the specified symbol.
    """
    params = {
        "symbol": symbol,
        "startTime": str(exchange.parse8601(start_time)),
        "limit": limit,
    }
    data = exchange.fapiPublicGetFundingRate(params)
    columns = ["Timestamp", "fundingRate", "symbol"]
    return extract_columns(data, columns)


def get_top_long_short_account_ratio(
    exchange, symbol: str, start_time: datetime, period: str = "1h", limit: int = 500
) -> List[dict]:
    """
    Get top long/short account ratio for a specific symbol.

    Args:
        exchange: The exchange instance.
        symbol (str): The symbol to retrieve the data for.
        start_time (datetime): The start time of the data.
        period (str, optional): The period of the data (default: "1h").
        limit (int, optional): The number of data points to retrieve (default: 500).

    Returns:
        List[dict]: The top long/short account ratio data for the specified symbol.
    """
    params = {
        "symbol": symbol,
        "period": period,
        "startTime": str(exchange.parse8601(start_time)),
        "limit": limit,
    }
    data = exchange.fapiDataGetTopLongShortAccountRatio(params)
    columns = ["Timestamp", "AR_longAccount", "AR_longShortRatio", "AR_shortAccount"]
    return extract_columns(data, columns)


def get_top_long_short_position_ratio(
    exchange, symbol: str, start_time: datetime, period: str = "1h", limit: int = 500
) -> List[dict]:
    """
    Get top long/short position ratio for a specific symbol.

    Args:
        exchange: The exchange instance.
        symbol (str): The symbol to retrieve the data for.
        start_time (datetime): The start time of the data.
        period (str, optional): The period of the data (default: "1h").
        limit (int, optional): The number of data points to retrieve (default: 500).

    Returns:
        List[dict]: The top long/short position ratio data for the specified symbol.
    """
    params = {
        "symbol": symbol,
        "period": period,
        "startTime": str(exchange.parse8601(start_time)),
        "limit": limit,
    }
    data = exchange.fapiDataGetTopLongShortPositionRatio(params)
    columns = ["Timestamp", "PR_longAccount", "PR_longShortRatio", "PR_shortAccount"]
    return extract_columns(data, columns)


def get_global_long_short_account_ratio(
    exchange,
    symbol: str,
    start_time: datetime,
    period: str = "1h",
    limit: int = 500,
) -> List[dict]:
    """
    Get global long/short account ratio for a specific symbol.

    Args:
        exchange: The exchange instance.
        symbol (str): The symbol to retrieve the data for.
        start_time (datetime): The start time of the data.
        period (str, optional): The period of the data (default: "1h").
        limit (int, optional): The number of data points to retrieve (default: 500).

    Returns:
        List[dict]: The global long/short account ratio data for the specified symbol.
    """
    params = {
        "symbol": symbol,
        "period": period,
        "startTime": str(exchange.parse8601(start_time)),
        "limit": limit,
    }
    data = exchange.fapiDataGetGlobalLongShortAccountRatio(params)
    columns = ["Timestamp", "GAR_longAccount", "GAR_longShortRatio", "GAR_shortAccount"]
    return extract_columns(data, columns)


def get_taker_long_short_ratio(
    exchange, symbol: str, start_time: datetime, period: str = "1h", limit: int = 500
) -> List[dict]:
    """
    Get taker long/short ratio for a specific symbol.

    Args:
        exchange: The exchange instance.
        symbol (str): The symbol to retrieve the data for.
        start_time (datetime): The start time of the data.
        period (str, optional): The period of the data (default: "1h").
        limit (int, optional): The number of data points to retrieve (default: 500).

    Returns:
        List[dict]: The taker long/short ratio data for the specified symbol.
    """
    params = {
        "symbol": symbol,
        "period": period,
        "startTime": str(exchange.parse8601(start_time)),
        "limit": limit,
    }
    data = exchange.fapiDataGetTakerlongshortRatio(params)
    columns = ["Timestamp", "buySellRatio", "sellVol", "buyVol"]
    return extract_columns(data, columns)
