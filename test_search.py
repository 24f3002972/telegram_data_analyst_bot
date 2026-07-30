from dotenv import load_dotenv
load_dotenv()

from search import search_public_data

results = search_public_data(
    "Which state has the highest maternal mortality rate?"
)

for r in results:
    print("=" * 80)
    print(r["title"])
    print(r["url"])

    if "content" in r:
        print(r["content"][:500])