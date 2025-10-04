import requests

SOURCE_PROFILES = {
  "literature": {
    "base_url": "https://www.gutenberg.org/ebooks/search/",
    "params": {
      "sort_order": "downloads",
      "filetype": "txt",
      "language": "en"
    },
    "type": "gutenberg"
  },
  "crowdsourced": {
    "base_url": "https://commonvoice.mozilla.org/en/datasets",
    "type": "tsv"
  }
}

# Get Search Results
def get_search_results(params):
  response = requests.get(SEARCH_URL, params=params)
  if response.status_code == 200:
    return response.text
  else:
    raise Exception(f"Search failed: {response.status_code}")


def filter_corpus():
  print("Filtering corpus from /corpus_seed/seed_data.json")
  