import pandas as pd
import requests
import re
from io import BytesIO, StringIO


def extract_urls(text):
    pattern = r"https?://[^\s]+"
    return re.findall(pattern, text)


def load_dataset(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    lower = url.lower()

    if lower.endswith(".csv"):
        return pd.read_csv(StringIO(response.text))

    if lower.endswith(".xlsx") or lower.endswith(".xls"):
        return pd.read_excel(BytesIO(response.content))

    if lower.endswith(".json"):
        return pd.read_json(BytesIO(response.content))

    return None