from skillbench.emulator import Emulator
from trueskill import TrueSkill
import itertools
import math
import matplotlib.pyplot as plt
from skillbench.data import Team, TeamPair


class RandomEmulator(Emulator):
    def __init__(self, random):
        super().__init__()
        self.random = random
        pass

    def emulate(self, team1, team2):
        return self.random.random()

    def fit_one_match(self, teams: TeamPair, winner: Team):
        super().fit_one_match(teams, winner)
        pass

    @property
    def name(self):
        return "RandomEmulator"
