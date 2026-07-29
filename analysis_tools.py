import pandas as pd


def dataset_info(df):

    return {
        "rows": len(df),
        "columns": list(df.columns),
        "types": df.dtypes.astype(str).to_dict()
    }


def numeric_columns(df):

    return list(
        df.select_dtypes(include="number").columns
    )


def categorical_columns(df):

    return list(
        df.select_dtypes(exclude="number").columns
    )

def statistics(df):

    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        return {}

    return {

        "mean": numeric.mean().to_dict(),

        "median": numeric.median().to_dict(),

        "min": numeric.min().to_dict(),

        "max": numeric.max().to_dict(),

        "sum": numeric.sum().to_dict(),

        "count": numeric.count().to_dict()
    }

def preview(df):

    return df.head(10).to_markdown(index=False)

def dataframe_context(df):

    return f"""

Dataset Information

{dataset_info(df)}

Statistics

{statistics(df)}

Preview

{preview(df)}
"""