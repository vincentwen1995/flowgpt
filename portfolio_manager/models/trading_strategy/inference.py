import asyncio
import concurrent.futures
import math
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import List

import click
import pandas as pd
from data_sources.exchange_data.binance import (
    fetch_exchange_data,
    get_klines,
    load_symbols,
)
from data_sources.fuse_data import create_latest_features
from data_sources.mine_factors import mine_factors_from_files
from data_sources.social_media.reddit import get_popular_posts
from models.backtest import get_strategy_backtest_results
from utils.chatgpt import (
    chunk_string,
    num_tokens_from_messages,
    prompt_chatgpt_stream,
    num_tokens_from_string,
    prompt_chatgpt,
)
from utils.config_loader import ConfigLoader
from utils.dynaconf_utils import settings


def prepare_messages(data: str, factors: List[str]) -> dict:
    factors_text = []
    for factor_name in factors:
        with open(
            Path(settings.ROOT_PATH_FOR_DYNACONF)
            / settings.FACTORS_DIR
            / f"{factor_name}.py",
            "r",
        ) as py_file:
            factors_text.append(py_file.read())

    factors_all = "\n".join(factors_text)

    return [
        {"role": "system", "content": "You are a financial analysis assistant."},
        {
            "role": "user",
            "content": f"Given the following market data, news and social media data about the cryptocurrency market\n```\n{data}\n```\n\nplease concisely advise on assigning 1 weight (STRICTLY in format i.e. [0.1, 0.5, 0.4...]) to each of the following {len(factors)} factors:\n```python\n{factors_all}\n```\n",
        },
    ]


def seek_advise_for_factor_combinations(features: str, factors: List[str]):
    chatgpt_model = settings.CHATGPT_MODEL
    token_limit = settings.CHATGPT_TOKEN_LIMIT

    messages = prepare_messages(features, factors)
    num_token = num_tokens_from_messages(messages)
    message_overhead = num_token - num_tokens_from_string(features)
    print(f"{message_overhead=}")
    print(f"Input has {num_token} tokens.")
    if num_token > token_limit:
        batch = math.ceil(num_token / (token_limit - message_overhead))
        print(f"Chunking into {batch} batches.")
        requests = 0
        for sub_text in chunk_string(features, batch):
            try:
                messages = prepare_messages(sub_text, factors)
                print(f"Chunked message tokens: {num_tokens_from_messages(messages)}")
                result = prompt_chatgpt_stream(
                    messages,
                    model=chatgpt_model,
                )
                print(f"Returned message:\n{result['content']}")
                requests += 1
            except Exception as e:
                print(e)
                continue
            if requests > settings.INFERENCE_LIMIT_FOR_DEMO:
                break
        return

    try:
        result = prompt_chatgpt_stream(
            messages,
            model=chatgpt_model,
        )
        print(f"Returned message:\n{result['content']}")
        requests += 1
    except Exception as e:
        print(e)


def strategy_inference(start_dt, end_dt, config_loader):
    chatgpt_model = settings.CHATGPT_MODEL
    token_limit = settings.CHATGPT_TOKEN_LIMIT

    aggregated_info = create_latest_features()

    # TODO: Seek advise for selecting factors.
    factors = ["manual_factor_0", "manual_factor_1", "manual_factor_2"]

    seek_advise_for_factor_combinations(aggregated_info, factors)

    history_data_per_symbol = fetch_exchange_data(start_dt, end_dt)
    history_data = pd.DataFrame()
    for symbol, symbol_df in history_data_per_symbol.items():
        # history_data = history_data.append(symbol_df, ignore_index=True)
        history_data = pd.concat([history_data, symbol_df], ignore_index=True)

    # get_strategy_backtest_results()
