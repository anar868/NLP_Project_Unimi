import time
import requests

CROSSREF_URL = "https://api.crossref.org/works"

def get_dois(
    issn: str,
    from_year: int,
    to_year: int,
    rows: int = 200,
    max_items: int = 400
):
    dois = []
    cursor = "*" 

    while True:
        params = {
            "filter": f"issn:{issn},from-pub-date:{from_year}-01-01,until-pub-date:{to_year}-12-31",
            "cursor": cursor,
            "rows": rows,
            "select": "DOI",
        }

        r = requests.get(CROSSREF_URL, params=params, timeout=60)

        msg = r.json().get("message", {})
        items = msg.get("items", [])
        if not items:
            break

        for it in items:
            doi = it.get("DOI")
            if doi:
                dois.append(doi.lower())

        dois = list(dict.fromkeys(dois))  
        print(f"DOIs collected so far: {len(dois)}")

        if len(dois) >= max_items:
            break

        next_cursor = msg.get("next-cursor")
        if not next_cursor or next_cursor == cursor:
            break

        cursor = next_cursor
        time.sleep(1.0)  

    return dois