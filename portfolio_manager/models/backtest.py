from importlib import import_module

from typing import List
import itertools

import numpy as np
import pandas as pd

from utils.dynaconf_utils import settings
from utils.config_loader import ConfigLoader


def min_max_scaling(df, column):
    min_value = df[column].min()
    max_value = df[column].max()
    df[column] = (df[column] - min_value) / (max_value - min_value)
    return df


def process_data(df, select_coin_num, factor_name, window):
    df["timestamp"] = df["Timestamp"]
    df["open"].fillna(method="ffill", inplace=True)
    df["high"].fillna(method="ffill", inplace=True)
    df["low"].fillna(method="ffill", inplace=True)

    df["Mtm"] = (df["close"] / df["close"].shift(window) - 1) * 100

    df["bottom"] = df.groupby("timestamp")[factor_name].rank(method="first")
    df["top"] = df.groupby("timestamp")[factor_name].rank(
        method="first", ascending=False
    )

    df["direction"] = df.apply(
        lambda x: 1
        if x["top"] <= select_coin_num
        else (-1 if x["bottom"] <= select_coin_num else 0),
        axis=1,
    )
    df = df[df["direction"] != 0]

    df["weights"] = 1.0
    df["factor"] = factor_name

    df = df[
        [
            "symbol",
            "timestamp",
            "top",
            "bottom",
            "direction",
            "weights",
            "factor",
        ]
    ]
    df.sort_values(by=["timestamp", "direction"], ascending=[True, False], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def cal_ind(select_c):
    if select_c.empty:
        return None

    results = pd.DataFrame()
    results.loc[0, "cumulative_net_value"] = round(
        select_c["capital_curve"].iloc[-1], 2
    )

    select_c["max2here"] = select_c["capital_curve"].expanding().max()
    select_c["dd2here"] = select_c["capital_curve"] / select_c["max2here"] - 1

    end_date, max_drawdown = select_c.sort_values(by=["dd2here"]).iloc[0][
        ["candle_begin_time", "dd2here"]
    ]
    start_date = (
        select_c[select_c["candle_begin_time"] <= end_date]
        .sort_values(by="capital_curve", ascending=False)
        .iloc[0]["candle_begin_time"]
    )

    results.loc[0, "maximum_drawdown"] = format(max_drawdown, ".2%")
    results.loc[0, "maximum_drawdown_start_time"] = str(start_date)
    results.loc[0, "maximum_drawdown_end_time"] = str(end_date)

    results.loc[0, "profit_period_count"] = len(
        select_c.loc[select_c["return_rate"] > 0]
    )
    results.loc[0, "loss_period_count"] = len(
        select_c.loc[select_c["return_rate"] <= 0]
    )
    results.loc[0, "win_rate"] = format(
        results.loc[0, "profit_period_count"] / len(select_c), ".2%"
    )
    results.loc[0, "average_period_return"] = format(
        select_c["return_rate"].mean(), ".2%"
    )
    results.loc[0, "profit_loss_ratio"] = round(
        select_c.loc[select_c["return_rate"] > 0]["return_rate"].mean()
        / select_c.loc[select_c["return_rate"] <= 0]["return_rate"].mean()
        * (-1),
        2,
    )
    results.loc[0, "maximum_period_profit"] = format(
        select_c["return_rate"].max(), ".2%"
    )
    results.loc[0, "maximum_period_loss"] = format(select_c["return_rate"].min(), ".2%")

    results.loc[0, "maximum_continuous_profit_period_count"] = max(
        [
            len(list(v))
            for k, v in itertools.groupby(
                np.where(select_c["return_rate"] > 0, 1, np.nan)
            )
        ]
    )
    results.loc[0, "maximum_continuous_loss_period_count"] = max(
        [
            len(list(v))
            for k, v in itertools.groupby(
                np.where(select_c["return_rate"] <= 0, 1, np.nan)
            )
        ]
    )

    time_during = (
        select_c.iloc[-1]["candle_begin_time"] - select_c.iloc[0]["candle_begin_time"]
    )
    total_seconds = time_during.days * 24 * 3600 + time_during.seconds
    if total_seconds == 0:
        annual_return = 0
    else:
        final_r = round(select_c["capital_curve"].iloc[-1], 2)
        annual_return = pow(final_r, 24 * 3600 * 365 / total_seconds) - 1

    results.loc[0, "annual_return"] = str(round(annual_return, 2)) + " times"
    results.loc[0, "annual_return_drawdown_ratio"] = round(
        (annual_return) / abs(max_drawdown), 2
    )

    return results, select_c


def evaluate(df, c_rate, select_coin_num):
    df["return_rate1"] = (
        -(1 * c_rate) + 1 * (1 + df["ret_next"] * df["direction"]) * (1 - c_rate) - 1
    )
    select_coin = pd.DataFrame()
    select_coin["return_rate"] = df.groupby("candle_begin_time")[
        "return_rate1"
    ].sum() / (select_coin_num * 2)
    select_coin.reset_index(inplace=True)
    return select_coin


def backtest(hold_hour, c_rate, select_coin_num, select_coin):
    select_coin["candle_begin_time"] = pd.to_datetime(select_coin["candle_begin_time"])

    temp = pd.DataFrame()
    for offset, g_df in select_coin.groupby("offset"):
        print(offset)
        g_df.sort_values(by="candle_begin_time", inplace=True)
        g_df.reset_index(drop=True, inplace=True)
        select_c = evaluate(g_df, c_rate, select_coin_num)
        select_c["capital_curve"] = (select_c["return_rate"] + 1).cumprod()
        select_c["offset"] = offset
        rtn, select_c = cal_ind(select_c)
        print(rtn)
        # temp = temp.append(rtn, ignore_index=True)
        temp = pd.concat([temp, rtn], ignore_index=True)

    all_select_df = evaluate(select_coin, c_rate, select_coin_num)
    all_select_df["return_rate"] = all_select_df["return_rate"] / int(hold_hour[:-1])
    all_select_df["capital_curve"] = (all_select_df["return_rate"] + 1).cumprod()
    rtn, select_c = cal_ind(all_select_df)
    # temp = temp.append(rtn)
    temp = pd.concat([temp, rtn], ignore_index=True)
    print(
        'Average "Annualized Return/Drawdown Ratio" for all offsets: ',
        temp["annual_return_drawdown_ratio"][:-1].mean(),
    )
    return temp


def compute_factors(market_data_df: pd.DataFrame, factor_weights: dict, window: int):
    market_data_df["combined_factor"] = 0
    for factor_name, weight in factor_weights.items():
        factor_module = import_module(f"models.factors.{factor_name}")
        market_data_df[factor_name] = factor_module.signal(
            df=market_data_df, window=window, factor_name=factor_name
        )
        market_data_df = min_max_scaling(market_data_df, factor_name)
        market_data_df["combined_factor"] += market_data_df[factor_name] * weight
        market_data_df.drop(columns=[factor_name], inplace=True)

    return market_data_df


def get_strategy_backtest_results(
    market_data_df: pd.DataFrame,
    factor_weights: dict,
    strategy_config: str,
    config_loader: ConfigLoader,
):
    strategy_conf = config_loader.get_config(strategy_config)
    if not strategy_conf:
        raise Exception(
            f"Specified strategy configuration {strategy_config} not found."
        )
    coin_num = strategy_conf["coin_num"]
    window = strategy_conf["window"]
    hold_hour = strategy_conf["hold_hour"]
    c_rate = strategy_conf["c_rate"]
    ranking_df = compute_factors(market_data_df, factor_weights, window)
    ranking_df = process_data(ranking_df, coin_num, "combined_factor", window)
    return backtest(hold_hour, c_rate, coin_num, ranking_df)
