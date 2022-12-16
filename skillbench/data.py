from typing import List
from enum import Enum

class Team:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Team({self.name})"

class Outcome(Enum):
    TEAM1 = 1
    TEAM2 = 2
    DRAW = 3

    def __repr__(self):
        return f"Outcome({self.name})"

class Match:
    def __init__(self, matchId: int, timestamp: int, team1: Team, team2: Team, outcome: Outcome):
        self.matchId = matchId
        self.timestamp = timestamp
        self.team1 = team1
        self.team2 = team2
        self.outcome = outcome

    def __repr__(self):
        return f"Match({self.matchId}, {self.timestamp}, {self.team1}, {self.team2}, {self.outcome})"

class MatchDataset:
    def __init__(self, matches: List[Match]):
        self.matches = matches
    
    # Read from csv, expecting format: matchId, timestamp, team1, team2, outcome
    def __init__(self, matches_csv_path: str):
        self.matches = []
        with open(matches_csv_path, 'r') as f:
            for line in f:
                matchId, timestamp, team1, team2, outcome = line.split(',')
                self.matches.append(Match(int(matchId), int(timestamp), Team(team1), Team(team2), Outcome(outcome)))

    # Split dataset into two, according to timestamp
    def split(self, train_ratio: float):
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
        return f"MatchDataset({self.matches})"

