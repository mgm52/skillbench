from .. import Emulator
from trueskill import TrueSkill
import itertools
import math
import matplotlib.pyplot as plt
from skillbench.data import Team, TeamPair


class RandomEmulator(Emulator):
    def __init__(self, random):
        self.random = random
        pass

    def emulate(self, team1, team2):
        return self.random.random()

    def fit_one_match(self, teams: TeamPair, winner: Team):
        pass

    @property
    def name(self):
        return "RandomEmulator"
