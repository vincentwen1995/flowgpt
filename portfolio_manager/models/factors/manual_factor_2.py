def signal(df, window, factor_name):
    df["oma"] = df["open"].ewm(span=window, adjust=False).mean()
    df["hma"] = df["high"].ewm(span=window, adjust=False).mean()
    df["ima"] = df["low"].ewm(span=window, adjust=False).mean()
    df["cma"] = df["close"].ewm(span=window, adjust=False).mean()
    df["tp"] = (df["oma"] + df["hma"] + df["ima"] + df["cma"]) / 4
    df["ma"] = df["tp"].ewm(span=window, adjust=False).mean()
    df["abs_diff_close"] = abs(df["tp"] - df["ma"])
    df["md"] = df["abs_diff_close"].ewm(span=window, adjust=False).mean()
    df[factor_name] = (df["tp"] - df["ma"]) / (df["md"] + 1e-8)

    df.drop(
        columns=["oma", "hma", "ima", "cma", "tp", "ma", "abs_diff_close", "md"],
        inplace=True,
    )

    return df
