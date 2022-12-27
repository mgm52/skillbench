from collections import defaultdict
from typing import List
from enum import Enum
import pandas as pd


class Team:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Team({self.name})"

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

        # with open(matches_csv_path, 'r') as f:
        # for line in f:
        # matchId, timestamp, team_won, team_lost, score_won, score_lost = line.split(',')
        # if score_won > score_lost:
        #     outcome = Outcome.TEAM1
        # else:
        #     outcome = Outcome.DRAW
        # self.matches.append(Match(int(matchId), int(timestamp), Team(team_won), Team(team_lost), outcome))

    # Split dataset into two, according to timestamp
    def split(self, train_ratio: float):
        print(f"Split: {train_ratio}")
        self.matches.sort(key=lambda match: match.timestamp)
        split_idx = int(len(self.matches) * train_ratio)
        return MatchDataset(self.matches[:split_idx]), MatchDataset(self.matches[split_idx:])

    def __len__(self):
        return len(self.matches)

    def __getitem__(self, idx):
        return self.matches[idx]

    def __iter__(self):
        return iter(self.matches)

    def __repr__(self):
        return f"<MatchDataset: {len(self.matches)} matches>"
