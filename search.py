import os
from tavily import TavilyClient

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_public_data(question):

    query = f"""
    India MOSPI data.gov.in Sample Registration System
    {question}
    site:mospi.gov.in OR site:pib.gov.in OR site:data.gov.in
    """

    result = client.search(
        query=query,
        topic="general",
        search_depth="advanced",
        max_results=5,
    )

    return result["results"]