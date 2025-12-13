import requests
from bs4 import BeautifulSoup
import csv

def convert_height(h):
    if not h or h.strip() in ("-", ""):
        return None
    h = h.replace("’", "-").replace("'", "-").replace('"', "").strip()
    parts = h.split("-")
    if len(parts) != 2:
        return None
    try:
        return int(parts[0]) * 12 + int(parts[1])
    except ValueError:
        return None


def scrape_table_school(url, school, name_col, height_col):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    players = []

    for row in soup.select("table tbody tr"):
        cols = row.find_all("td")
        if len(cols) > max(name_col, height_col):
            name = cols[name_col].get_text(strip=True)
            height_raw = cols[height_col].get_text(strip=True)
            height_in = convert_height(height_raw)
            if name:
                players.append([school, name, height_raw, height_in])
    return players


def main():
    all_players = []

    all_players += scrape_table_school(
        "https://yorkathletics.com/sports/womens-volleyball/roster",
        "York College", 1, 3
    )

    all_players += scrape_table_school(
        "https://bmccathletics.com/sports/womens-volleyball/roster",
        "BMCC", 1, 3
    )

    all_players += scrape_table_school(
        "https://hostosathletics.com/sports/womens-volleyball/roster",
        "Hostos CC", 1, 3
    )

    all_players += scrape_table_school(
        "https://bronxbroncos.com/sports/womens-volleyball/roster/2021",
        "Bronx CC", 1, 3
    )

    all_players += scrape_table_school(
        "https://queensknights.com/sports/womens-volleyball/roster",
        "Queens College", 1, 3
    )

    all_players += scrape_table_school(
        "https://augustajags.com/sports/wvball/roster",
        "Augusta College", 1, 4
    )

    all_players += scrape_table_school(
        "https://flaglerathletics.com/sports/womens-volleyball/roster",
        "Flagler College", 1, 3
    )

    all_players += scrape_table_school(
        "https://pacersports.com/sports/womens-volleyball/roster",
        "USC Aiken", 1, 3
    )

    all_players += scrape_table_school(
        "https://www.golhu.com/sports/womens-volleyball/roster",
        "Penn State - Lock Haven", 1, 4
    )

    with open("womens_volleyball.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["School", "Name", "Height Raw", "Height (inches)"])
        writer.writerows(all_players)

    heights = [p[3] for p in all_players if p[3] is not None]
    if heights:
        print("Average height:", round(sum(heights) / len(heights), 2))
    else:
        print("No valid height data")

    print("Saved", len(all_players), "players to womens_volleyball.csv")


if __name__ == "__main__":
    main()
import csv

heights = []

with open("womens_volleyball.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row["Height (inches)"]:
            heights.append(int(row["Height (inches)"]))

if heights:
    average_height = sum(heights) / len(heights)
    print(f"Average height for women's volleyball players: {average_height:.2f} inches")
else:
    print("No valid height data found.")
