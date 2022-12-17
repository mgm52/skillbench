# Get match data from the HLTV.org
import time
from bs4 import BeautifulSoup
import requests

def download_matches():
    print("Downloading matches...")
    matches = []
    for page in range(1):
        print(f"Downloading page {page}...")

        headers = {
            'referer': 'www.hltv.org/stats',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

        cookies = {
            "hltvTimeZone": "Europe/Copenhagen"
        }

        url = f"https://www.hltv.org/results?offset={page * 100}&startDate=2022-01-01&endDate=2022-12-31&stars=2"
        soup = BeautifulSoup(requests.get(url, headers=headers, cookies=cookies).text, "lxml")
        print(soup)
        for match in soup.find_all("div", class_="results"):
            print(match)
            # match_id = match["id"].split("-")[1]
            # team1 = match.find("div", class_="team1-gradient").find("div", class_="logo").find("img")["alt"]
            # team2 = match.find("div", class_="team2-gradient").find("div", class_="logo").find("img")["alt"]
            # outcome = match.find("div", class_="result-score").text
            # matches.append((match_id, team1, team2, outcome))
    print("Done downloading matches")
    return matches

print(download_matches())
