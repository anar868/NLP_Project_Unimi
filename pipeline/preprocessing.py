import re

def normalize_whitespace(s: str) -> str:
    return re.sub(r"\s+", " ", str(s)).strip()

def preprocess_df(df, year_min=2016, year_max=2026, min_words=30):
    df = df.copy()
    df = df[df["year"].between(year_min, year_max)]
    df["abstract"] = df["abstract"].apply(normalize_whitespace)
    df = df[df["abstract"].str.split().apply(len) >= min_words]
    df = df.drop_duplicates(subset=["doi"])
    df = df.drop_duplicates(subset=["abstract"])
    return df