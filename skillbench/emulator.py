from abc import ABC, abstractmethod
from skillbench.data import Team, TeamPair
from typing import Optional

# Abstract class representing an emulator. Trueskill and others can subclass this
class Emulator(ABC):
    @abstractmethod
    def emulate(self, team1: Team, team2: Team) -> float:
        "Returns the emulated probability that team1 beats team2 (maybe we need to model draws too)"
        pass

    @abstractmethod
    def fit_one_match(self, teams: TeamPair, winner: Optional[Team]):
        "Given some ground truth match data, update the emulator's internals using it"
        # Expect each subclass to call super().fit_one_match(teams, winner) to update the fit counts
        # TODO: consider whether there's a better way to do this...
        for team in teams:
            self.team_fit_count[team] = self.team_fit_count.get(team, 0) + 1
            for player in team.players:
                self.player_fit_count[player] = self.player_fit_count.get(player, 0) + 1
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def __init__(self):
        # Expect each subclass to call super().__init__() to initialize the fit counts
        # TODO: consider whether there's a better way to do this...
        self.team_fit_count = {}
        self.player_fit_count = {}
        #print(f"Initialized Emulator")