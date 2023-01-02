from .. import Emulator
from trueskill import TrueSkill
import itertools
import math
import matplotlib.pyplot as plt
from skillbench.data import Team, TeamPair


class WinRateEmulator(Emulator):
    def __init__(self):
        self.wins = {}
        self.matches_seen = {}
        self.maxtotal = 0
        pass

    def emulate(self, team1, team2):
        wr1 = 0.5 if (not team1 in self.matches_seen) else (self.wins.get(team1, 0) / self.matches_seen.get(team1))
        wr2 = 0.5 if (not team2 in self.matches_seen) else (self.wins.get(team2, 0) / self.matches_seen.get(team2))
        winprob = (wr1 - wr2) / 2 + 0.5
        return winprob

    def fit_one_match(self, teams: TeamPair, winner: Team):
        team1, team2 = teams
        self.matches_seen[team1] = self.matches_seen.get(team1, 0) + 1
        self.matches_seen[team2] = self.matches_seen.get(team2, 0) + 1
        self.maxtotal = max(self.maxtotal, self.matches_seen[team1], self.matches_seen[team2])
        if winner is not None:
            self.wins[winner] = self.wins.get(winner, 0) + 1
        # Count draw as loss for both teams

    def acquisition_function(self, teams):
        # Preference for smaller totals
        team1, team2 = teams
        return self.maxtotal - min(self.matches_seen.get(team1, 0), self.matches_seen.get(team2, 0))

    @property
    def name(self):
        return "WinRateEmulator"

    def visualize(self):
        teams = list(self.matches_seen.keys())
        teams.sort(key=lambda x: x.name.lower())
        team_names = [t.name for t in teams]
        wrs = [(self.wins.get(team, 0) / self.matches_seen.get(team)) for team in teams]

        plt.errorbar(wrs, team_names, xerr=0, fmt='o')
        plt.axvline(x=0.5, color='r', linestyle='--')
        plt.title("WinRateEmulator winrates")
        plt.legend(["Initial winrate", "Team winrate"])
        plt.show()
