import json
from pandas_analysis import dataframe_context
from memory import add_message, get_history
from logger import log_event
from intent_parser import get_analysis_plan
from operations import execute_plan
from search import search_public_data
from json_utils import (
    extract_json_template,
    extract_json_response,
)
from data_loader import (
    extract_urls,
    load_dataset,
)
from ai import ask_llm
LOG_URL = "https://telegramdataanalystbot-production-78b7.up.railway.app/run.jsonl"

def solve(chat_id, question):

    template = extract_json_template(question)
    print("TEMPLATE =", template)
    log_event("received_message", question)

    add_message(chat_id, question)

    messages = get_history(chat_id)

    if len(messages) > 3:
        history = "\n".join(messages[-3:])
    else:
        history = "\n".join(messages)

    urls = extract_urls(question)

    log_event("urls_found", urls)

    dataset_text = ""
    analysis_result = None
    search_results = None
    search_text = ""

    if not urls:
        search_results = search_public_data(question)
        log_event("search_results", search_results)
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
            planning_question = question

            if template:
                planning_question = planning_question.replace(
                    json.dumps(template),
                    ""
                )

            plan = get_analysis_plan(
                planning_question,
                list(df.columns)
            )
            log_event("analysis_plan", plan)

            analysis_result = execute_plan(
                df,
                plan
            )
            print("ANALYSIS RESULT =", analysis_result)
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
    if search_results:

        for item in search_results[:1]:
  
            search_text += f"""
Title:
{item['title']}

URL:
{item['url']}

Content:
{item['content']}

"""
    if analysis_result is not None:

        prompt = f"""
You are a JSON formatter.

The data analysis has already been completed.

DO NOT perform any calculations.
DO NOT guess.
DO NOT use previous conversation.

Current Question:
{question}

Computed Analysis Result:
{analysis_result}
"""

    else:

        prompt = f"""
You are a professional data analyst.

Answer the user's question using the information below.

Priority:

1. Analysis Result
2. Dataset
3. Public Search Results

If Public Search Results are provided,
use ONLY those results.
Do not use prior knowledge or memory.

Prefer these sources:

1. mospi.gov.in
2. data.gov.in
3. pib.gov.in

Do NOT guess.
Do NOT invent values.

Question:
{history}

Dataset:
{dataset_text}

Public Search Results:
{search_text}
"""

    if template:

        prompt += f"""

Return ONLY ONE valid JSON object.

Use this exact JSON structure:

{json.dumps(template, indent=2)}

Do NOT change the structure.
Do NOT add explanations.
Do NOT use markdown.
"""
 
    else:

        prompt += """

Return ONLY the requested answer.
"""

    log_event("sending_to_llm", prompt[:3000])
    if analysis_result is not None and template:

    # analysis_result may be a list or a dict
        if isinstance(analysis_result, list):
            first = analysis_result[0]
        elif isinstance(analysis_result, dict):
            first = analysis_result
        else:
            first = {"value": analysis_result}

        result = {
            "answer": {},
            "log_url": LOG_URL
        }

    # Fill answer according to template keys
        print("FIRST =", first)
        for key in template["answer"]:

            matched = False

            for col in first:

                if key.lower() == col.lower():

                    result["answer"][key] = first[col]
                    matched = True
                    break

        # If no matching column, use generic value
            if not matched and "value" in first:
                result["answer"][key] = first["value"]

        return json.dumps(result, separators=(",", ":"))
    raw_answer = ask_llm(prompt)

    log_event("llm_answer", raw_answer)

    result = extract_json_response(raw_answer)
    if result is not None:
        result["log_url"] = LOG_URL
    if result is None:

        result = {
            "answer": raw_answer,
            "log_url": LOG_URL,
        }

    if "answer" not in result:

        result = {
            "answer": result,
            "log_url": LOG_URL,
        }

    if "log_url" not in result:

        result["log_url"] = LOG_URL

    return json.dumps(
        result,
        separators=(",", ":"),
    )