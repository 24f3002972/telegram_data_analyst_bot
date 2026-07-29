from data_loader import extract_urls, load_dataset

text = """
Download this dataset

https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv
"""

urls = extract_urls(text)

print(urls)

df = load_dataset(urls[0])

print(df.head())