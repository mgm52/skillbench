# Get match data from the HLTV.org
import time
import datetime
import json


def download_matches():
    from bs4 import BeautifulSoup
    import requests

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


def download_matches_per_player():
    from bs4 import BeautifulSoup
    import requests

    print("Downloading matches...")
    matches = {}
    for page in range(1):
        print(f"Downloading page {page}...")

        headers = {
            'referer': 'www.hltv.org/stats',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

        cookies = {
            "hltvTimeZone": "Europe/London"
        }

        url = f"https://www.hltv.org/results?offset={page * 100}&startDate=2017-01-01&endDate=2022-12-31&content=stats&stars=2"
        soup = BeautifulSoup(requests.get(url, headers=headers, cookies=cookies).text, "lxml")
        all_results = soup.find("div", {"class": "allres"})
        for days_results in all_results.find_all("div", class_="results-sublist"):
            for match in days_results.find_all("div", class_="result-con"):
                url_suffix = match.find("a", class_="a-reset")["href"]
                match_id = match.find("a", class_="a-reset")["href"].split("/")[2]
                match_stats = {}
                sub_soup = BeautifulSoup(
                    requests.get(f"https://www.hltv.org{url_suffix}", headers=headers, cookies=cookies).text, "lxml")

                try:
                    match_stats["team1"] = sub_soup.find("div", class_="teamsBox").find("div",
                                                                                        class_="team1-gradient").find(
                        "div",
                        class_="teamName").text
                    match_stats["team2"] = sub_soup.find("div", class_="teamsBox").find("div",
                                                                                        class_="team2-gradient").find(
                        "div",
                        class_="teamName").text
                    match_stats["timestamp"] = int(
                        sub_soup.find("div", class_="teamsBox").find("div", class_="timeAndEvent").find("div",
                                                                                                        class_="date")[
                            "data-unix"])
                    try:
                        match_stats["team1_score"] = int(sub_soup.find("div", class_="team1-gradient").find("div",
                                                                                                            class_="won").text)
                        match_stats["team2_score"] = int(sub_soup.find("div", class_="team2-gradient").find("div",
                                                                                                            class_="lost").text)
                    except:
                        match_stats["team1_score"] = int(sub_soup.find("div", class_="team1-gradient").find("div",
                                                                                                            class_="lost").text)
                        match_stats["team2_score"] = int(sub_soup.find("div", class_="team2-gradient").find("div",
                                                                                                            class_="won").text)

                except:
                    print(url_suffix)

                maps = {}
                for map in sub_soup.find_all("div", class_="mapholder"):
                    try:
                        map_id = map.find("a", class_="results-stats")["href"].split("/")[4]
                        team1_score = int(
                            map.find("div", class_="results-left").find("div", class_="results-team-score").text)
                        team2_score = int(
                            map.find("span", class_="results-right").find("div", class_="results-team-score").text)
                        maps[map_id] = {}
                        maps[map_id]["name"] = map.find("div", class_="mapname").text
                        maps[map_id]["team1_score"] = team1_score
                        maps[map_id]["team2_score"] = team2_score
                    except:
                        continue

                stats = sub_soup.find("div", class_="matchstats")
                for div in stats.find_all("div", class_="stats-content"):
                    if div["id"].split("-")[0] in maps:
                        maps[div["id"].split("-")[0]]["stats"] = {}
                        team1_players = {}
                        team2_players = {}
                        count = 0
                        for team in div.find_all("table", class_="totalstats"):
                            for player in team.find_all("tr"):
                                if "header-row" in player["class"]:
                                    count += 1
                                    continue
                                player_name = player.find("span", class_="player-nick").text
                                player_stats = {}
                                # print(player.find("td", class_="kd"))
                                player_stats["kills"] = int(player.find("td", class_="kd").text.split("-")[0])
                                player_stats["deaths"] = int(player.find("td", class_="kd").text.split("-")[1])
                                player_stats["adr"] = float(player.find("td", class_="adr").text)
                                player_stats["rating"] = float(player.find("td", class_="rating").text)
                                if count == 1:
                                    team1_players[player_name] = player_stats
                                if count == 2:
                                    team2_players[player_name] = player_stats
                        # print(team1_players, team2_players)
                        maps[div["id"].split("-")[0]]["stats"]["team1"] = team1_players
                        maps[div["id"].split("-")[0]]["stats"]["team2"] = team2_players
                        match_stats["maps"] = maps

                matches[match_id] = match_stats
                print(f"Downloaded match {match_id}")
                time.sleep(0.5)
                # break
            # break
        time.sleep(2)
    print("Done downloading matches")
    return matches


if __name__ == '__main__':
    matches = download_matches_per_player()
    print(json.dumps(matches, indent=4))

    with open('../Dataset/dataset2.json', 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=4)
