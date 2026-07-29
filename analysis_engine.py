import json
from pandas_analysis import dataframe_context
from memory import add_message, get_history
from logger import log_event
from intent_parser import get_analysis_plan
from operations import execute_plan
from json_utils import (
    extract_json_template,
    extract_json_response,
)
from data_loader import (
    extract_urls,
    load_dataset,
)
from ai import ask_llm


def solve(chat_id, question):

    template = extract_json_template(question)

    log_event("received_message", question)

    add_message(chat_id, question)

    history = "\n".join(get_history(chat_id))

    urls = extract_urls(question)

    log_event("urls_found", urls)

    dataset_text = ""
    analysis_result = None

    if urls:

        try:

            df = load_dataset(urls[0])
            log_event(
                    "dataset_loaded",
                    {
                        "rows": len(df),
                        "columns": list(df.columns),
                    },
            )
            plan = get_analysis_plan(
                question,
                list(df.columns)
            )

            log_event("analysis_plan", plan)

            analysis_result = execute_plan(
                df,
                plan
             )

            log_event(
                "analysis_result",
                str(analysis_result)
            )


            dataset_text = dataframe_context(df)
            if analysis_result is not None:
                dataset_text += f"""

            Analysis Result

            {analysis_result}
            """

        except Exception as e:

            log_event("dataset_error", str(e))

            dataset_text = f"Dataset could not be loaded: {e}"

    prompt = f"""
You are a professional data analyst.

Question:
{history}

Dataset:
{dataset_text}
"""

    if template:

        prompt += f"""

Return ONLY ONE valid JSON object.

It MUST match this structure exactly:

{json.dumps(template, indent=2)}

Never wrap the JSON in markdown.

Return one JSON object only.
"""

    else:

        prompt += """

Return ONLY the requested answer.
"""

    log_event("sending_to_llm", prompt[:3000])

    raw_answer = ask_llm(prompt)

    log_event("llm_answer", raw_answer)

    result = extract_json_response(raw_answer)

    if result is None:

        result = {
            "answer": raw_answer,
            "log_url": "PLACEHOLDER",
        }

    if "answer" not in result:

        result = {
            "answer": result,
            "log_url": "PLACEHOLDER",
        }

    if "log_url" not in result:

        result["log_url"] = "PLACEHOLDER"

    return json.dumps(
        result,
        separators=(",", ":"),
    )