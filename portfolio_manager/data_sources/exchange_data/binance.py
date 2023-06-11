from datetime import datetime, timedelta
from typing import List

import ccxt
import pandas as pd
from utils.dynaconf_utils import settings
from utils.dt_utils import datetime_range

binance = ccxt.binance()
remove_list = set(settings.BINANCE_UNWANTED_SYMBOLS)


def load_symbols() -> List[str]:
    """
    Load symbols from the binance.

    Returns:
        List[str]: A list of symbols.
    """
    binance_info = binance.fapiPublicGetbinanceInfo()
    symbol_list = list(
        filter(
            lambda x: bool(x),
            [
                symbol["symbol"]
                if symbol["contractType"] == "PERPETUAL"
                and symbol["symbol"] not in remove_list
                and symbol["symbol"].endswith("USDT")
                else None
                for symbol in binance_info["symbols"]
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
    symbol: str,
    start_time: datetime,
    interval: str = "1h",
    limit: int = 500,
) -> List[dict]:
    """
    Get Klines (candlestick) data for a specific symbol.

    Args:
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
        "startTime": str(binance.parse8601(start_time)),
        "limit": limit,
    }
    data = binance.fapiPublicGetKlines(params=params)
    columns = [
        "symbol",
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


def get_funding_rate(symbol: str, start_time: datetime, limit: int = 500) -> List[dict]:
    """
    Get funding rates for a specific symbol.

    Args:
        symbol (str): The symbol to retrieve the funding rates for.
        start_time (datetime): The start time of the funding rates.
        limit (int, optional): The number of funding rates to retrieve (default: 500).

    Returns:
        List[dict]: The funding rates data for the specified symbol.
    """
    params = {
        "symbol": symbol,
        "startTime": str(binance.parse8601(start_time)),
        "limit": limit,
    }
    data = binance.fapiPublicGetFundingRate(params)
    columns = ["Timestamp", "fundingRate", "symbol"]
    return extract_columns(data, columns)


def get_top_long_short_account_ratio(
    symbol: str, start_time: datetime, period: str = "1h", limit: int = 500
) -> List[dict]:
    """
    Get top long/short account ratio for a specific symbol.

    Args:
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
        "startTime": str(binance.parse8601(start_time)),
        "limit": limit,
    }
    data = binance.fapiDataGetTopLongShortAccountRatio(params)
    columns = ["Timestamp", "AR_longAccount", "AR_longShortRatio", "AR_shortAccount"]
    return extract_columns(data, columns)


def get_top_long_short_position_ratio(
    symbol: str, start_time: datetime, period: str = "1h", limit: int = 500
) -> List[dict]:
    """
    Get top long/short position ratio for a specific symbol.

    Args:
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
        "startTime": str(binance.parse8601(start_time)),
        "limit": limit,
    }
    data = binance.fapiDataGetTopLongShortPositionRatio(params)
    columns = ["Timestamp", "PR_longAccount", "PR_longShortRatio", "PR_shortAccount"]
    return extract_columns(data, columns)


def get_global_long_short_account_ratio(
    symbol: str,
    start_time: datetime,
    period: str = "1h",
    limit: int = 500,
) -> List[dict]:
    """
    Get global long/short account ratio for a specific symbol.

    Args:
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
        "startTime": str(binance.parse8601(start_time)),
        "limit": limit,
    }
    data = binance.fapiDataGetGlobalLongShortAccountRatio(params)
    columns = ["Timestamp", "GAR_longAccount", "GAR_longShortRatio", "GAR_shortAccount"]
    return extract_columns(data, columns)


def get_taker_long_short_ratio(
    symbol: str, start_time: datetime, period: str = "1h", limit: int = 500
) -> List[dict]:
    """
    Get taker long/short ratio for a specific symbol.

    Args:
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
        "startTime": str(binance.parse8601(start_time)),
        "limit": limit,
    }
    data = binance.fapiDataGetTakerlongshortRatio(params)
    columns = ["Timestamp", "buySellRatio", "sellVol", "buyVol"]
    return extract_columns(data, columns)


def aggregate_data(symbol: str, date_list: List[datetime]) -> pd.DataFrame:
    """
    Aggregate data for a symbol and a list of dates.

    Args:
        symbol (str): The symbol to retrieve the data for.
        date_list (List[datetime]): A list of dates to aggregate data for.

    Returns:
        pd.DataFrame: The aggregated data as a pandas DataFrame.
    """
    data = pd.DataFrame()

    for start_time in date_list:
        klines = get_klines(symbol, start_time)
        # funding_rate = get_funding_rate(symbol, start_time)
        # top_long_short_account_ratio = get_top_long_short_account_ratio(
        #     symbol, start_time
        # )
        # top_long_short_position_ratio = get_top_long_short_position_ratio(
        #     symbol, start_time
        # )
        # global_long_short_account_ratio = get_global_long_short_account_ratio(
        #     symbol, start_time
        # )
        # taker_long_short_ratio = get_taker_long_short_ratio(symbol, start_time)

        df = pd.DataFrame(klines)

        df["MTS"] = pd.to_numeric(df["MTS"])  # Cast "MTS" column to numeric type
        df["Timestamp"] = pd.to_datetime(df["MTS"], unit="ms")
        df = df[
            [
                "symbol",
                "Timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "quote_volume",
                "trade_num",
                "taker_buy_base_asset_volume",
                "taker_buy_quote_asset_volume",
            ]
        ]

        # df = pd.merge(df, pd.DataFrame(funding_rate), on="Timestamp", how="left")
        # df["fundingRate"] = df["fundingRate"].fillna(method="ffill")
        # df["symbol"] = df["symbol"].fillna(method="ffill")

        # df = pd.merge(
        #     df, pd.DataFrame(top_long_short_account_ratio), on="Timestamp", how="left"
        # )

        # df = pd.merge(
        #     df, pd.DataFrame(top_long_short_position_ratio), on="Timestamp", how="left"
        # )

        # df = pd.merge(
        #     df,
        #     pd.DataFrame(global_long_short_account_ratio),
        #     on="Timestamp",
        #     how="left",
        # )

        # df = pd.merge(
        #     df, pd.DataFrame(taker_long_short_ratio), on="Timestamp", how="left"
        # )

        # data = data.append(df, ignore_index=True)
        data = pd.concat([data, df], ignore_index=True)

    data.drop_duplicates(subset=["Timestamp"], keep="last", inplace=True)
    data.sort_values("Timestamp", inplace=True)
    data.reset_index(drop=True, inplace=True)

    return data


def fetch_exchange_data(start_dt: datetime, end_dt: datetime) -> dict:
    symbols = None
    if settings.BINANCE_SYMBOLS:
        symbols = settings.BINANCE_SYMBOLS
    else:
        symbols = load_symbols()
    return {
        symbol: aggregate_data(
            symbol,
            date_list=[
                dt for dt in datetime_range(start_dt, end_dt, timedelta(days=1))
            ],
        )
        for symbol in symbols
    }


def fetch_latest_exchange_data() -> dict:
    return fetch_exchange_data(
        start_dt=datetime.today().replace(hour=0, minute=0, second=0, microsecond=0),
        end_dt=datetime.today().replace(hour=0, minute=0, second=0, microsecond=0),
    )
