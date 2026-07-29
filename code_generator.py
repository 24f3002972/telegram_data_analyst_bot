from ai import ask_llm


def generate_pandas_code(question, df):

    columns = list(df.columns)

    prompt = f"""
You are a pandas expert.

DataFrame name is df.

Columns:

{columns}

Question:

{question}

Return ONLY ONE valid Python pandas expression.

Rules

- Do not explain.
- Do not use print().
- Do not use markdown.
- Return only one expression.
- Expression must use dataframe df.
"""

    return ask_llm(prompt).strip()

