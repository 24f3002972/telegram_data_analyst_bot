import pandas as pd

from operations import execute_plan

df = pd.DataFrame({
    "State": ["Kerala", "Tamil Nadu", "Karnataka"],
    "Population": [35, 70, 65]
})

plan = {
    "operation": "mean",
    "column": "Population"
}

print(execute_plan(df, plan))