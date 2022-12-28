from abc import ABC, abstractmethod

from skillbench.data import Team, TeamPair
from typing import Optional


# Abstract class representing an emulator. Trueskill and others can subclass this
class Emulator(ABC):
    @abstractmethod
    def emulate(team1: Team, team2: Team) -> float:
        "Returns the emulated probability that team1 beats team2 (maybe we need to model draws too)"
        pass

    @abstractmethod
    def fit_one_match(teams: TeamPair, winner: Optional[Team]):
        "Given some ground truth match data, update the emulator's internals using it"
        pass

    @abstractmethod
    def aquisition_function(teams: TeamPair) -> float:
        "The emulator's desire to know the outcome of this match. The emulator gets given the match it most wants to see"
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__
