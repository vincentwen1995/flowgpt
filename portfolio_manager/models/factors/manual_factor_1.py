def signal(df, n, factor_name):
    df["mtm"] = df["close"] / df["close"].shift(n) - 1
    df["volatility"] = (
        df["high"].rolling(n, min_periods=1).max()
        - df["low"].rolling(n, min_periods=1).min()
        - 1
    )
    df["hourly_volatility"] = df["high"] / df["low"] - 1
    df["hourly_volatility_mean"] = (
        df["hourly_volatility"].rolling(n, min_periods=1).mean()
    )
    df[factor_name] = df["mtm"].rolling(window=n, min_periods=1).mean() * (
        df["volatility"] + df["hourly_volatility_mean"]
    )

    df.drop(
        columns=["mtm", "volatility", "hourly_volatility", "hourly_volatility_mean"],
        inplace=True,
    )

    return df
