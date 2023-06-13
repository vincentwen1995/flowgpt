import asyncio
import pandas as pd
import concurrent.futures
from datetime import datetime
from time import sleep

import click
from data_sources.exchange_data.binance import (
    get_klines,
    load_symbols,
    fetch_exchange_data,
)
from utils.chatgpt import prompt_chatgpt_stream
from utils.config_loader import ConfigLoader
from utils.dynaconf_utils import settings
from data_sources.social_media.reddit import get_popular_posts
from data_sources.mine_factors import mine_factors_from_files
from data_sources.fuse_data import create_latest_features
from models.backtest import get_strategy_backtest_results
from models.trading_strategy.inference import strategy_inference


@click.group()
def cli():
    """Financial Portfolio Manager CLI"""
    pass


@cli.command()
def mine_factors():
    mine_factors_from_files()


@cli.command()
@click.option(
    "--start-dt",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Start date",
    required=True,
)
@click.option(
    "--end-dt",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="End date",
    required=True,
)
def infer_strategy(start_dt, end_dt):
    """Infer trading strategy"""
    click.echo(f"Starting trading strategy inference...")
    config_loader = ConfigLoader()
    config_loader.start()
    strategy_inference(start_dt, end_dt, config_loader)
    click.echo("Trading strategy inference complete.")


if __name__ == "__main__":
    cli()
