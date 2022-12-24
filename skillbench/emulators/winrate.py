from .. import Emulator
from trueskill import TrueSkill
import itertools
import math
import matplotlib.pyplot as plt
from skillbench.data import Team, TeamPair

class WinRateEmulator(Emulator):
  def __init__(self):
    self.wins = {}
    self.totals = {}
    self.maxtotal = 0
    pass
  
  def emulate(self, team1, team2):
    wr1 = 0.5 if (not team1 in self.totals) else (self.wins.get(team1, 0) / self.totals.get(team1))
    wr2 = 0.5 if (not team2 in self.totals) else (self.wins.get(team2, 0) / self.totals.get(team2))
    winprob = (wr1 - wr2) / 2 + 0.5
    return winprob

  def fit_one_match(self, teams: TeamPair, winner: Team):
    team1, team2 = teams
    self.totals[team1] = self.totals.get(team1, 0) + 1
    self.totals[team2] = self.totals.get(team2, 0) + 1
    self.maxtotal = max(self.maxtotal, self.totals[team1], self.totals[team2])
    if winner is not None:
      self.wins[winner] = self.wins.get(winner, 0) + 1
    # Count draw as loss for both teams
  
  def aquisition_function(self, teams):
    # Preference for smaller totals
    team1, team2 = teams
    return self.maxtotal - min(self.totals.get(team1, 0), self.totals.get(team2, 0))
  
  @property
  def name(self):
    return "WinRateEmulator"

  def visualize(self):
    teams = list(self.totals.keys())
    teams.sort(key = lambda x: x.name.lower())
    team_names = [t.name for t in teams]
    wrs = [(self.wins.get(team, 0) / self.totals.get(team)) for team in teams]

    plt.errorbar(wrs, team_names, xerr=0, fmt='o')
    plt.axvline(x=0.5, color='r', linestyle='--')
    plt.title("WinRateEmulator winrates")
    plt.legend(["Initial winrate", "Team winrate"])
    plt.show()