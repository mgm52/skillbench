from .. import Emulator
from collections import defaultdict
import matplotlib.pyplot as plt
from typing import Optional

from skillbench.data import Team, TeamPair


####### Elo class based on https://github.com/ddm7018/Elo/blob/master/elosports/elo.py under MIT license
class EloEmulator(Emulator):
    def __init__(self, k=10, mu=1500):
        self.k = k
        self.mu = mu

        self.ratings = defaultdict(lambda: self.mu)

    def emulate(self, team1, team2):
        exp = (self.ratings[team2] - self.ratings[team1]) / 400
        return 1 / (10 ** exp + 1)

    def fit_one_match(self, teams: TeamPair, winner: Optional[Team]):
        # Use outcome to update rating of each team (i.e. self.ratings)
        team1, team2 = teams
        prob = self.emulate(team1, team2)
        if winner == team1:
            self.ratings[team1] += self.k * (1 - prob)
            self.ratings[team2] += self.k * (0 - prob)
        elif winner == team2:
            self.ratings[team2] += self.k * (1 - prob)
            self.ratings[team1] += self.k * (0 - prob)
        else:
            pass # No update on draw

    def aquisition_function(self, teams):
        # TODO: use a better aquisition function
        return abs(0.5 - self.emulate(*teams))

    @property
    def name(self):
        return "Elo"

    def visualize(self):
        teams = list(self.ratings.keys())
        teams.sort(key=lambda x: x.name.lower())
        team_names = [t.name for t in teams]
        mus = [self.ratings.get(team) for team in teams]

        plt.errorbar(mus, team_names, fmt='o')
        plt.axvline(x=self.ts.mu, color='r', linestyle='--')
        plt.title("Elo ratings")
        plt.legend(["Initial avg rating", "Team rating $\mu$"])
        plt.show()
