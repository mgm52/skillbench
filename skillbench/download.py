# Get match data from the HLTV.org
import time
from bs4 import BeautifulSoup
import requests
import datetime
import csv

def download_matches():
    print("Downloading matches...")
    matches = []
    for page in range(4):
        print(f"Downloading page {page}...")

        headers = {
            'referer': 'www.hltv.org/stats',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

        cookies = {
            "hltvTimeZone": "Europe/London"
        }

        url = f"https://www.hltv.org/results?offset={page * 100}&startDate=2022-01-01&endDate=2022-12-31&stars=2"
        soup = BeautifulSoup(requests.get(url, headers=headers, cookies=cookies).text, "lxml")
        all_results = soup.find("div", {"class": "allres"})
        for days_results in all_results.find_all("div", class_="results-sublist"):
            day = days_results.text.split(" ")[2:5]
            day[2] = day[2][:4]
            day[1] = day[1][:-2]
            day = " ".join(day)
            day = datetime.datetime.strptime(day, "%B %d %Y")
            for match in days_results.find_all("div", class_="result-con"):
                match_id = match.find("a", class_="a-reset")["href"].split("/")[2]
                team1 = match.find("div", class_="team1")
                team2 = match.find("div", class_="team2")
                team_won = team1.find("div", class_="team-won")
                if team_won is None:
                    team_won = team2.find("div", class_="team-won").text
                    team_lost = team1.find("div", class_="team").text
                else:
                    team_won = team_won.text
                    team_lost = team2.find("div", class_="team").text

                score_won = match.find("span", {"class": "score-won"}).text
                score_lost = match.find("span", {"class": "score-lost"}).text
                # print(f"{team_won} {score_won} - {score_lost} {team_lost} on {day}")
                matches.append((day, match_id, team_won, score_won, score_lost, team_lost))
        time.sleep(0.5)
    print("Done downloading matches")
    return matches

matches = download_matches()

with open('../Dataset/dataset1.csv', 'a') as dataset:
    writer = csv.writer(dataset)
    for row in matches:
        writer.writerow(row)