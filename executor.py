def execute_expression(expression, df):

    allowed = {
        "df": df
    }
    blocked = [
        "import",
        "__",
        "open(",
        "exec(",
        "eval(",
        "os.",
        "sys.",
        "subprocess",
    ]

    for word in blocked:
        if word in expression:
            raise ValueError(f"Blocked expression: {word}")
    return eval(expression, {"__builtins__": {}}, allowed)