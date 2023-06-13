def signal(df, window, factor_name):
    df["mtm"] = df["close"] / df["close"].shift(window) - 1
    df["volatility"] = (
        df["high"].rolling(window, min_periods=1).max()
        - df["low"].rolling(window, min_periods=1).min()
        - 1
    )
    df["hourly_volatility"] = df["high"] / df["low"] - 1
    df["hourly_volatility_mean"] = (
        df["hourly_volatility"].rolling(window, min_periods=1).mean()
    )
    df[factor_name] = df["mtm"].rolling(window=window, min_periods=1).mean() * (
        df["volatility"] + df["hourly_volatility_mean"]
    )

    df.drop(
        columns=["mtm", "volatility", "hourly_volatility", "hourly_volatility_mean"],
        inplace=True,
    )

    return df
