def signal(df, n, factor_name):
    df["mean"] = df["close"].ewm(span=n, adjust=False, min_periods=1).mean()
    df["bias"] = df["close"] / df["mean"] - 1
    df["volhigh"] = df["volume"].rolling(n, min_periods=1).max()
    df["vollow"] = df["volume"].rolling(n, min_periods=1).min()
    df["regvol"] = (df["volume"] - df["vollow"]) / (df["volhigh"] - df["vollow"])
    df["bias2"] = df["bias"] * df["regvol"].rolling(window=n, min_periods=1).mean()
    df[factor_name] = df["bias2"].rolling(window=n, min_periods=1).mean()

    df.drop(
        columns=["bias2", "bias", "volhigh", "vollow", "regvol", "mean"], inplace=True
    )

    return df
