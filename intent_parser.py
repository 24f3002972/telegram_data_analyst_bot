import json

from ai import ask_llm
from json_utils import extract_json_response


def get_analysis_plan(question, columns):

    prompt = f"""
You are a data analyst.

Dataset columns:

{columns}

User question:

{question}

Return ONLY valid JSON.

Supported operations:

mean
median
sum
count
max
min
top
bottom
sort
group_mean
group_sum
value_counts
unique

Schema:

{{
  "operation":"",
  "column":"",
  "group_by":"",
  "ascending":true,
  "top_n":1
}}

Never explain.

Return JSON only.
"""

    response = ask_llm(prompt)

    result = extract_json_response(response)

    return result