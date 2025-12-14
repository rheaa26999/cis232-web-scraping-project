import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# ----------------------------
# Height conversion functions
# ----------------------------
def parse_height_to_inches(height_text):
    if pd.isna(height_text):
        return None

    s = str(height_text).strip()

    # matches 6-2 or 6'2 or 6`2
    match = re.search(r"(\d+)\s*[-'`]\s*(\d{1,2})", s)
    if match:
        feet = int(match.group(1))
        inches = int(match.group(2))
    else:
        # fallback: just a feet number
        match = re.search(r"(\d+)", s)
        if not match:
            return None
        feet = int(match.group(1))
        inches = 0

    return feet * 12 + inches


def parse_height_to_cm(height_text):
    inches = parse_height_to_inches(height_text)
    if inches is None:
        return None
    return inches * 2.54


# ---------------------------------------
# MEN'S SWIMMING roster URLs (your list)
# ---------------------------------------
mens_swim_urls = [
    ("College of Staten Island", "https://csidolphins.com/sports/mens-swimming-and-diving/roster"),
    ("York College", "https://yorkathletics.com/sports/mens-swimming-and-diving/roster"),
    ("Baruch College", "https://athletics.baruch.cuny.edu/sports/mens-swimming-and-diving/roster"),
    ("Brooklyn College", "https://www.brooklyncollegeathletics.com/sports/mens-swimming-and-diving/roster"),
    ("Lindenwood University", "https://lindenwoodlions.com/sports/mens-swimming-and-diving/roster"),
    ("McKendree University", "https://mckbearcats.com/sports/mens-swimming-and-diving/roster"),
    ("Ramapo College", "https://ramapoathletics.com/sports/mens-swimming-and-diving/roster"),
    ("SUNY Oneonta", "https://oneontaathletics.com/sports/mens-swimming-and-diving/roster"),
    ("SUNY Binghamton", "https://bubearcats.com/sports/mens-swimming-and-diving/roster/2021-22"),
    ("Albright College", "https://albrightathletics.com/sports/mens-swimming-and-diving/roster/2021-22"),
]


def scrape_one_mens_swim_roster(school_name, url):
    print(f"Scraping {school_name} ...")

    response = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    html = response.text

    # try to read tables from the page
    try:
        tables = pd.read_html(html)
    except ValueError:
        print(f"  -> No HTML tables found for {school_name}. Skipping.")
        return pd.DataFrame(columns=["name", "height_raw", "school", "height_in"])

    roster_table = None

    # pick the first table that contains a height column
    for t in tables:
        cols_lower = [str(c).lower() for c in t.columns]
        if any(("ht" in c) or ("height" in c) or ("hgt" in c) for c in cols_lower):
            roster_table = t
            break

    if roster_table is None:
        print(f"  -> No table with height column found for {school_name}. Skipping.")
        return pd.DataFrame(columns=["name", "height_raw", "school", "height_in"])

    # find name + height columns
    name_col = None
    height_col = None

    for col in roster_table.columns:
        col_lower = str(col).lower()
        if name_col is None and ("name" in col_lower or "player" in col_lower or "athlete" in col_lower):
            name_col = col
        if height_col is None and ("ht" in col_lower or "height" in col_lower or "hgt" in col_lower):
            height_col = col

    # fallback: if it didn’t detect name col, use first col
    if name_col is None:
        name_col = roster_table.columns[0]

    if height_col is None:
        print(f"  -> Could not find height column for {school_name}. Skipping.")
        return pd.DataFrame(columns=["name", "height_raw", "school", "height_in"])

    temp = roster_table[[name_col, height_col]].copy()
    temp.columns = ["name", "height_raw"]
    temp["school"] = school_name

    # convert + keep valid heights only
    temp["height_in"] = temp["height_raw"].apply(parse_height_to_inches)
    temp = temp[temp["height_in"].notna()].copy()

    return temp[["name", "height_raw", "school", "height_in"]]


# ----------------------------
# Run scrape for all schools
# ----------------------------
all_rosters = []

for school, url in mens_swim_urls:
    df_school = scrape_one_mens_swim_roster(school, url)
    all_rosters.append(df_school)

mens_swim_df = pd.concat(all_rosters, ignore_index=True)

if mens_swim_df.empty:
    print("ERROR: No rows scraped. Rosters may not be in HTML tables on these sites.")
else:
    mens_swim_df["sport"] = "swimming"
    mens_swim_df["gender"] = "M"
    mens_swim_df["team"] = "Men's Swimming"
    mens_swim_df["height_cm"] = mens_swim_df["height_in"] * 2.54

    print("\nFirst few rows:")
    print(mens_swim_df.head())

    print("\nNumber of players scraped:", len(mens_swim_df))

    avg_height_in = mens_swim_df["height_in"].mean()
    avg_height_cm = mens_swim_df["height_cm"].mean()

    print("\nAverage men's swimming height:")
    print(f"{avg_height_in:.2f} inches  (~ {avg_height_cm:.2f} cm)")

    # save to your project data folder
    mens_swim_df = mens_swim_df[
        ["name", "height_raw", "school", "sport", "gender", "team", "height_in", "height_cm"]
    ]
    mens_swim_df.to_csv("data/mens_swim.csv", index=False)
print("\nSaved file: data/mens_swim.csv")



