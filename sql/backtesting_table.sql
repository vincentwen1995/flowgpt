CREATE TABLE backtesting_performance
(
    id SERIAL PRIMARY KEY,
    cumulative_net_value DECIMAL(10, 2),
    maximum_drawdown TEXT,
    maximum_drawdown_start_timestamp TIMESTAMP WITHOUT TIME ZONE,
    maximum_drawdown_end_timestamp TIMESTAMP WITHOUT TIME ZONE,
    profit_periods INT,
    loss_periods INT,
    win_rate TEXT,
    average_profit_per_period TEXT,
    profit_loss_ratio DECIMAL(10, 2),
    max_profit_in_single_period TEXT,
    max_loss_in_single_period TEXT,
    max_consecutive_profit_periods INT,
    max_consecutive_loss_periods INT,
    annualized_return TEXT,
    annualized_return_drawdown_ratio DECIMAL(10, 2),
    strategy_code_md5 TEXT,
    start_dt TIMESTAMP,
    end_dt TIMESTAMP,
    insert_dt TIMESTAMP,
    INDEX idx_strategy_code_interval (strategy_code_md5, start_dt, end_dt)
);
