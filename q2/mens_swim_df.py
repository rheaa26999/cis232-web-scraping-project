import pandas as pd
import requests
from bs4 import BeautifulSoup

rosters = {
    "College of Staten Island": "https://csidolphins.com/sports/mens-swimming-and-diving/roster",
    "York College": "https://yorkathletics.com/sports/mens-swimming-and-diving/roster",
    "Baruch College": "https://athletics.baruch.cuny.edu/sports/mens-swimming-and-diving/roster",
    "Brooklyn College": "https://www.brooklyncollegeathletics.com/sports/mens-swimming-and-diving/roster",
    "Lindenwood University": "https://lindenwoodlions.com/sports/mens-swimming-and-diving/roster",
    "McKendree University": "https://mckbearcats.com/sports/mens-swimming-and-diving/roster",
    "Ramapo College": "https://ramapoathletics.com/sports/mens-swimming-and-diving/roster",
    "SUNY Oneonta": "https://oneontaathletics.com/sports/mens-swimming-and-diving/roster",
    "SUNY Binghamton": "https://bubearcats.com/sports/mens-swimming-and-diving/roster/2021-22",
    "Albright College": "https://albrightathletics.com/sports/mens-swimming-and-diving/roster/2021-22",
}

rows_out = []

for school, url in rosters.items():
    print(f"Scraping: {school}")
    r = requests.get(url, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) >= 2:
            name = tds[0].get_text(strip=True)
            height = tds[1].get_text(strip=True)

            if name and height:
                rows_out.append({"school": school, "name": name, "height": height})

df = pd.DataFrame(rows_out)

print("\nPreview:")
print(df.head(10))
print(f"\nTotal rows scraped: {len(df)}")

df.to_csv("data/mens_swim.csv", index=False)
print("Saved CSV to data/mens_swim.csv")

