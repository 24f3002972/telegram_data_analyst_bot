import pandas as pd


def dataframe_summary(df):
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "numeric_columns": list(df.select_dtypes(include="number").columns),
        "categorical_columns": list(df.select_dtypes(exclude="number").columns),
    }

def statistics(df):

    stats = {}

    numeric = df.select_dtypes(include="number")

    if not numeric.empty:
        stats["mean"] = numeric.mean().to_dict()
        stats["min"] = numeric.min().to_dict()
        stats["max"] = numeric.max().to_dict()
        stats["sum"] = numeric.sum().to_dict()

    return stats

def dataframe_context(df):

    summary = dataframe_summary(df)

    stats = statistics(df)

    preview = df.head(20).to_markdown(index=False)

    return f"""
Dataset Summary

{summary}

Statistics

{stats}

Preview

{preview}
"""