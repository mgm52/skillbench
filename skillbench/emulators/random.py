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

    def aquisition_function(self, teams):
        # No preference for any match
        return 0.5

    @property
    def name(self):
        return "RandomEmulator"
