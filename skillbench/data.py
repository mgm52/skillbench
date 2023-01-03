from collections import defaultdict
from typing import List, Optional
from enum import Enum
import pandas as pd
import json


class Team:
    def __init__(self, name: str, players: Optional[List[str]]=None):
        self.name = name
        self.players = players

    def has_players(self):
        return self.players is not None

    def __repr__(self):
        return f"Team({self.name}{'+' if self.has_players() else ''})"

    def __eq__(self, other):
        return False if other is None else self.name == other.name

    def __hash__(self):
        return hash(self.name)


class TeamPair:
    def __init__(self, team1: Team, team2: Team, random):
        self._teams_set = frozenset((team1, team2))
        if team1 == team2:
            raise ValueError(f"Matchup must be between two different teams, not {team1} vs {team2}")
        self._teams_list = random.sample(self._teams_set, 2)

    def __repr__(self):
        return f"Matchup({self._teams_set})"

    def __eq__(self, other):
        return self._teams_set == other._teams_set

    def __hash__(self):
        return hash(self._teams_set)

    # Define how to iterate over a Matchup
    def __iter__(self):
        return iter(self._teams_list)


class Match:
    def __init__(self, matchId: int, timestamp: int, teams: TeamPair, winner: Team):
        self.matchId = matchId
        self.timestamp = timestamp
        self.teams = teams
        self.winner = winner

    @property
    def team1(self):
        return self.teams._teams_list[0]

    @property
    def team2(self):
        return self.teams._teams_list[1]

    @property
    def loser(self):
        if self.winner is None: return None
        return self.team2 if self.winner == self.team1 else self.team1

    def __repr__(self):
        return f"Match({self.matchId}, {self.timestamp}, {self.teams}, {self.winner})"


class MatchDataset:
    # TODO: validation that match ids are unique
    def __init__(self, matches: List[Match]):
        self.matches = matches

        self.matchups: dict[TeamPair, List[Match]] = defaultdict(list)
        self.teams: dict[Team, List[Match]] = defaultdict(list)
        draws = 0
        for match in matches:
            self.matchups[match.teams].append(match)
            for team in match.teams:
                self.teams[team].append(match)
            if match.winner is None: draws += 1

        print(
            f"Loaded dataset of {len(matches)} matches ({100 * draws / len(matches):.2g}% draws, {len(self.teams)} teams, at least {min(len(ms) for ms in self.teams.values())} matches per team)")

    def __iter__(self):
        return iter(self.matches)

    def copy(self):
        print("Copying dataset")
        return MatchDataset(self.matches.copy())

    def filter_teams(self, min_games=1) -> "MatchDataset":
        """Filter out teams that have played less than min_games"""
        team_counter = defaultdict(int)
        for match in self.matches:
            team_counter[match.team1] += 1
            team_counter[match.team2] += 1

        teams_to_keep = set(team for team, count in team_counter.items() if count >= min_games)
        print(f"Filtering out teams with less than {min_games} games: {len(teams_to_keep)} teams remaining")

        new_matches = [match for match in self.matches if match.team1 in teams_to_keep and match.team2 in teams_to_keep]
        return MatchDataset(new_matches)

    # Read from csv, expecting format: matchId, timestamp, team1, team2, outcome
    @classmethod
    def from_csv(cls, matches_csv_path: str, random):
        print(f"Csv: {matches_csv_path}")
        matches = []

        df = pd.read_csv(matches_csv_path)
        # print(df)
        if set(df.columns).issuperset(set(['date', 'id', 'team_won', 'team_lost', 'score_won', 'score_lost'])):
            for _, row in df.iterrows():
                if row['team_won'] == row['team_lost']:
                    print(f"WARNING: Match between same teams ({row['team_won']}), skipping")
                    continue
                winner = Team(row['team_won'])
                matches.append(
                    Match(int(row['id']), row['date'], TeamPair(Team(row['team1']), Team(row['team2']), random),
                          winner))

        elif set(df.columns).issuperset(set(['date', 'id', 'team1', 'team2', 'score1', 'score2'])):
            for _, row in df.iterrows():
                if row['team1'] == row['team2']:
                    print(f"WARNING: Match between same teams ({row['team1']}), skipping")
                    continue
                if row['score1'] > row['score2']:
                    winner = Team(row['team1'])
                elif row['score1'] < row['score2']:
                    winner = Team(row['team2'])
                else:
                    winner = None
                matches.append(
                    Match(int(row['id']), row['date'], TeamPair(Team(row['team1']), Team(row['team2']), random),
                          winner))

        return cls(matches)

    @classmethod
    def from_json(cls, matches_json_path: str, random):
        d = json.load(open(matches_json_path, 'r'))

        matches = []

        sorted_match_objects = sorted(d.items(), key=lambda match: match[1]['timestamp'])
        for match_id, match in sorted_match_objects:
            try:
                # For our IDs, we combine the team ID and team names to have both globally unique and readable
                team1_name = f"{match['team1_id']}-{match['team1']}"
                team2_name = f"{match['team2_id']}-{match['team2']}"

                # Combine players across maps
                team1_players = set()
                team2_players = set()
                for map_id, map in match['maps'].items():
                    for player_id, player_stats in map['stats']['team1'].items():
                        team1_players.add(player_id + '-' + player_stats['name'])
                    for player_id, player_stats in map['stats']['team2'].items():
                        team2_players.add(player_id + '-' + player_stats['name'])

                # Create teams
                team1 = Team(team1_name, list(team1_players))
                team2 = Team(team2_name, list(team2_players))

                if match['team1_score'] > match['team2_score']:
                    winner = team1
                elif match['team1_score'] < match['team2_score']:
                    winner = team2
                else:
                    winner = None

                matches.append(Match(match_id, match['timestamp'], TeamPair(team1, team2, random), winner))
            except Exception as e:
                print(match_id, "failed to load.")
                continue

        return cls(matches)


    # Split dataset into two, according to timestamp
    def split(self, train_ratio: float, random: Optional[int]=None):
        from sklearn.model_selection import train_test_split
        self.matches.sort(key=lambda match: match.timestamp)
        if random:
            print(f"Split: {train_ratio}, randomly with seed {random}")
            train_matches, test_matches = train_test_split(self.matches, train_size=train_ratio, shuffle=True, random_state=random)
        else:
            print(f"Split: {train_ratio}, by timestamp")
            train_matches, test_matches = train_test_split(self.matches, train_size=train_ratio, shuffle=False)

        return MatchDataset(train_matches), MatchDataset(test_matches)

    def __len__(self):
        return len(self.matches)

    def __getitem__(self, idx):
        return self.matches[idx]

    def __iter__(self):
        return iter(self.matches)

    def __repr__(self):
        return f"<MatchDataset: {len(self.matches)} matches>"
