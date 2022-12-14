from typing import List
from enum import Enum

class Team:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Team({self.name})"

# Define an outcome enum (team1/team2/draw)
class Outcome(Enum):
    TEAM1 = 1
    TEAM2 = 2
    DRAW = 3

    def __repr__(self):
        return f"Outcome({self.name})"

class Match:
    def __init__(self, team1: Team, team2: Team, outcome: Outcome):
        self.team1 = team1
        self.team2 = team2
        self.outcome = outcome

    def __repr__(self):
        return f"Match({self.team1}, {self.team2}, {self.outcome})"

class MatchDataset:
    def __init__(self, matches: List[Match]):
        self.matches = matches

    def __len__(self):
        return len(self.matches)

    def __getitem__(self, idx):
        return self.matches[idx]

    def __iter__(self):
        return iter(self.matches)

    def __repr__(self):
        return f"MatchDataset({self.matches})"

