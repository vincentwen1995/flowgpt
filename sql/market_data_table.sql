CREATE TABLE market_data_raw (
    id SERIAL PRIMARY KEY,
    title TEXT,
    source TEXT,
    published_at TIMESTAMP,
    data JSONB,
    insert_dt TIMESTAMP,
    INDEX idx_source_insert_dt (source, insert_dt)
);

CREATE TABLE processed_market_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP ,
    open_price DECIMAL(14, 2) ,
    high_price DECIMAL(14, 2) ,
    low_price DECIMAL(14, 2) ,
    close_price DECIMAL(14, 2) ,
    volume DECIMAL(14, 2) ,
    quote_volume DECIMAL(14, 2) ,
    trade_num INTEGER ,
    taker_buy_base_asset_volume DECIMAL(14, 2) ,
    taker_buy_quote_asset_volume DECIMAL(14, 2) ,
    funding_rate DECIMAL(10, 4) ,
    symbol VARCHAR(10) ,
    source TEXT,
    insert_dt TIMESTAMP,
    INDEX idx_source_symbol_timestamp (source, symbol, timestamp)
)