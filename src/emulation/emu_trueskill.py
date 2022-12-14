from emulator import Emulator
from trueskill import TrueSkill
import itertools
import math
from data.match import Team, Outcome

# An example emulator.
class TrueSkillEmulator(Emulator):
  def __init__(self, mu, sigma):
    self.ts = TrueSkill(mu, sigma)
    self.ratings = {}

  def emulate(self, team1, team2):
    # TODO: decide whether we're modelling each team as a list of players (as this func is currently written) or a single player
    # TODO: alter this function to use self.ratings, rather than expecting rating to be in team1 and team2 already
    # This function was written by Juho Snellman https://github.com/sublee/trueskill/issues/1#issuecomment-149762508
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (self.ts.beta * self.ts.beta) + sum_sigma)
    return self.ts.cdf(delta_mu / denom)

  def fit_one_match(team1: Team, team2: Team, outcome: Outcome):
    # TODO: use outcome to update rating of each team (i.e. self.ratings)
    pass
  
  def aquisition_function(self, team1, team2):
    # TODO: use a better aquisition function
    return math.abs(0.5 - self.emulate(team1, team2))