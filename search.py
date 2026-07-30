import os
from tavily import TavilyClient
 
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
 
PREFERRED_DOMAINS = ["mospi.gov.in", "data.gov.in", "pib.gov.in", "censusindia.gov.in"]
 
 
def search_public_data(question):
    query = f"{question} India state-wise official statistics"
 
    result = client.search(
        query=query,
        topic="general",
        search_depth="advanced",
        max_results=8,
        include_domains=PREFERRED_DOMAINS,
    )
 
    results = result.get("results", [])
 
    # Tavily's include_domains sometimes still returns a few off-domain hits;
    # if a preferred-domain result exists, always rank it first so the same
    # question doesn't get answered from a different source on every run.
    def sort_key(item):
        url = item.get("url", "")
        on_preferred = any(domain in url for domain in PREFERRED_DOMAINS)
        return (not on_preferred, -item.get("score", 0))
 
    results.sort(key=sort_key)
 
    # Fall back to an unrestricted search only if the domain-restricted
    # search returned nothing usable.
    if not results:
        fallback = client.search(
            query=query,
            topic="general",
            search_depth="advanced",
            max_results=5,
        )
        results = fallback.get("results", [])
 
    return results