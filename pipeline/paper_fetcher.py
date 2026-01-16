import os, time, json
import pandas as pd
import requests

PAPER_URL = "https://api.semanticscholar.org/graph/v1/paper/DOI:"
FIELDS = "paperId,title,abstract,year,venue,url"

headers = {}

def get_papers(doi: str):
    url = PAPER_URL + doi
    params = {"fields": FIELDS}

    r = requests.get(url, params=params, headers=headers, timeout=60)

    if r.status_code == 200:
        return r.json()

    return None

def get_data(dois, checkpoint_path = "data/papers.jsonl"):
    rows = []
    
    # Getting loaded data
    seen = set()
    if os.path.exists(checkpoint_path):
        with open(checkpoint_path, "r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                seen.add(obj["doi"])
                rows.append(obj)
        print(f"Resuming from checkpoint: {len(rows)} rows already saved")

    if len(rows) >= 400:
        return pd.DataFrame(rows).drop_duplicates(subset=["doi"])

    for i, doi in enumerate(dois, 1):
        if doi in seen:
            continue

        data = get_papers(doi)
        if data and data.get("abstract"):
            obj = {
                "doi": doi,
                "paperId": data.get("paperId"),
                "title": data.get("title"),
                "year": data.get("year"),
                "venue": data.get("venue"),
                "abstract": data.get("abstract"),
                "url": data.get("url"),
            }
            rows.append(obj)

            with open(checkpoint_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")

        if i % 25 == 0:
            print(f"processed {i}/{len(dois)} DOIs, kept {len(rows)} with abstracts")

        time.sleep(0.15)

    return pd.DataFrame(rows).drop_duplicates(subset=["doi"])