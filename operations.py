import pandas as pd


def execute_plan(df, plan):
    operation = plan.get("operation", "").lower()
    column = plan.get("column")
    group_by = plan.get("group_by")
    top_n = int(plan.get("top_n", 1))

    # ---------- Basic statistics ----------

    if operation == "mean":
        return df[column].mean()

    if operation == "median":
        return df[column].median()

    if operation == "sum":
        return df[column].sum()

    if operation == "count":
        return len(df)

    # ---------- Maximum ----------

    if operation == "max":
        row = df.loc[df[column].idxmax()]
        return row.to_dict()

    # ---------- Minimum ----------

    if operation == "min":
        row = df.loc[df[column].idxmin()]
        return row.to_dict()

    # ---------- Top N ----------

    if operation == "top":
        return (
            df.sort_values(column, ascending=False)
              .head(top_n)
              .to_dict(orient="records")
        )

    # ---------- Bottom N ----------

    if operation == "bottom":
        return (
            df.sort_values(column)
              .head(top_n)
              .to_dict(orient="records")
        )

    # ---------- Sort ----------

    if operation == "sort":
        ascending = plan.get("ascending", True)

        return (
            df.sort_values(
                column,
                ascending=ascending
            ).to_dict(orient="records")
        )

    # ---------- Group Mean ----------

    if operation == "group_mean":

        return (
            df.groupby(group_by)[column]
            .mean()
            .to_dict()
        )

    # ---------- Group Sum ----------

    if operation == "group_sum":

        return (
            df.groupby(group_by)[column]
            .sum()
            .to_dict()
        )

    # ---------- Value Counts ----------

    if operation == "value_counts":

        return (
            df[column]
            .value_counts()
            .to_dict()
        )

    # ---------- Unique ----------

    if operation == "unique":

        return list(
            df[column].unique()
        )

    return {
        "error": f"Unsupported operation '{operation}'"
    }