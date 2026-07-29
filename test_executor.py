import pandas as pd

from code_generator import generate_pandas_code
from executor import execute_expression

df = pd.DataFrame(
    {
        "State": [
            "Kerala",
            "Tamil Nadu",
            "Karnataka"
        ],
        "Population": [
            35,
            70,
            65
        ]
    }
)

question = "Which state has highest population?"

code = generate_pandas_code(question, df)

print(code)

answer = execute_expression(code, df)

print(answer)