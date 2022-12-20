from typing import List
from enum import Enum
import pandas as pd

class Team:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Team({self.name})"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

class Outcome(Enum):
    TEAM1 = 1
    TEAM2 = 2
    DRAW = 3

    @classmethod
    def score(cls, score1, score2):
        if score1 > score2:
            return cls.TEAM1
        elif score1 < score2:
            return cls.TEAM2
        else:
            return cls.DRAW

    def __repr__(self):
        return f"Outcome({self.name})"

def flip_outcome(outcome: Outcome):
    if outcome == Outcome.TEAM1:
        return Outcome.TEAM2
    elif outcome == Outcome.TEAM2:
        return Outcome.TEAM1
    else:
        return Outcome.DRAW

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
    
    def __init__(self, matches: List[Match]):
        self.matches = matches

    def __iter__(self):
        return iter(self.matches)

    # Read from csv, expecting format: matchId, timestamp, team1, team2, outcome
    @classmethod
    def from_csv(cls, matches_csv_path: str):
        matches = []

        df = pd.read_csv(matches_csv_path)
        print(df)
        if set(df.columns).issuperset(set(['date', 'id', 'team_won', 'team_lost', 'score_won', 'score_lost'])):
            for _, row in df.iterrows():
                outcome = Outcome.score(row['score_won'], row['score_lost'])
                matches.append(Match(int(row['id']), row['date'], Team(row['team_won']), Team(row['team_lost']), outcome))

        elif set(df.columns).issuperset(set(['date', 'id', 'team1', 'team2', 'score1', 'score2'])):
            for _, row in df.iterrows():
                outcome = Outcome.score(row['score1'], row['score2'])
                matches.append(Match(int(row['id']), row['date'], Team(row['team2']), Team(row['team1']), outcome))

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

