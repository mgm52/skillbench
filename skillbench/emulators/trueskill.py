from .. import Emulator
from trueskill import TrueSkill
import itertools
import math
import matplotlib.pyplot as plt

from skillbench.data import Team, Outcome

class TrueSkillEmulator(Emulator):
  def __init__(self, mu, sigma):
    self.ts = TrueSkill(mu, sigma)
    self.ratings = {}

  def emulate(self, team1, team2):
    # Replace teams by their rating
    # Currently one rating per team
    team1 = [self.ratings.get(team1, self.ts.Rating())]
    team2 = [self.ratings.get(team2, self.ts.Rating())]

    # TODO: decide whether we're modelling each team as a list of players (as this func is currently written) or a single player
    # This function was written by Juho Snellman https://github.com/sublee/trueskill/issues/1#issuecomment-149762508
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (self.ts.beta * self.ts.beta) + sum_sigma)
    return self.ts.cdf(delta_mu / denom)

  def fit_one_match(self, team1: Team, team2: Team, outcome: Outcome):
    # Use outcome to update rating of each team (i.e. self.ratings)
    rating1 = self.ratings.get(team1, self.ts.Rating())
    rating2 = self.ratings.get(team2, self.ts.Rating())

    if outcome == Outcome.TEAM1:
      new_ratings = self.ts.rate([(rating1,), (rating2,)])
    elif outcome == Outcome.TEAM2:
      new_ratings = self.ts.rate([(rating2,), (rating1,)])[::-1] # order of ratings is reversed
    else:
      new_ratings = self.ts.rate([(rating1,), (rating2,)], drawn=True)
    #print(new_ratings)
    
    self.ratings[team1] = new_ratings[0][0]
    self.ratings[team2] = new_ratings[1][0]
  
  def aquisition_function(self, team1, team2):
    # TODO: use a better aquisition function
    return abs(0.5 - self.emulate(team1, team2))
  
  @property
  def name(self):
    return "TrueSkill"

  def visualize(self):
    teams = list(self.ratings.keys())
    teams.sort(key = lambda x: x.name.lower())
    team_names = [t.name for t in teams]
    mus = [self.ratings.get(team).mu for team in teams]
    sigmas = [self.ratings.get(team).sigma for team in teams]

    plt.errorbar(mus, team_names, xerr=sigmas, fmt='o')
    plt.axvline(x=self.ts.mu, color='r', linestyle='--')
    plt.title("TrueSkill ratings ($\mu \pm \sigma$)")
    plt.legend(["Initial avg rating", "Team rating $\mu \pm \sigma$"])
    plt.show()

