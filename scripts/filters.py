import re
import requests
import json

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

def fetch_gutenberg_search(url, params):
  try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text
  except requests.RequestException as e:
    print(f"[ERROR] Failed to fetch search results: {e}")

def extract_book_ids(html):
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(html, "html.parser")
  links = soup.select("li.booklink a.link")
  ids = []
  for link in links:
    href = link.get("href")
    if href and href.startswith("/ebooks/"):
      book_id = href.split("/")[-1]
      ids.append(book_id)
  return ids

def download_book(book_id):
  url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
  response = requests.get(url)
  if response.status_code ==200:
    return clean_gutenberg_text(response.text)
  else:
    return None

def clean_gutenberg_text(raw_text):
  start = raw_text.find("*** START OF")
  end = raw_text.find("*** END OF")
  return raw_text[start:end].strip()

def extract_dialogue(text):
  # Match lines with quotation marks (basic English style)
  pattern = r'"([^"]+)"|\"([^\"]+)\"'
  matches = re.findall(pattern, text)

  #Flatten and clean results
  dialogue_lines = [line.strip() for pair in matches for line in pair if line]
  return dialogue_lines

def extract_dialogue_from_commonvoice(tsv_path):
  import pandas as pd
  df = pd.read_csv(tsv_path, sep="\t")
  return df["sentence"].dropna().tolist()

def save_to_corpus(data, path):
  with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
  print(f"[INFO] Saved {len(data)} dialogue lines to {path}")

# Get Search Results
def get_search_results(source_key):
  profile = SOURCE_PROFILES.get(source_key)
  if not profile:
    raise ValueError(f"Unknown source type: {source_key}")
  
  if profile ["type"] == "gutenberg":
    html = fetch_gutenberg_search(profile["base_url"], profile["params"])
    book_ids = extract_book_ids(html)
    for book_id in book_ids:
      text = download_book(book_id)
      if text:
        dialogue = extract_dialogue(text)
        save_to_corpus(dialogue, f"corpus_seed/literature_{book_id}.json")

  elif profile["type"] == "tsv":
    dialogue = extract_dialogue_from_commonvoice("path/to/commonvoice.tsv")
    save_to_corpus(dialogue, "corpus_seed/dialogue_corpus.json")

def filter_corpus():
  print("Filtering corpus from /corpus_seed/seed_data.json")