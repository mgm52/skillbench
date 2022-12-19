from .. import Emulator
from trueskill import TrueSkill
import itertools
import math
import matplotlib.pyplot as plt
import random
from skillbench.data import Team, Outcome

class RandomEmulator(Emulator):
  def __init__(self):
    pass

  def emulate(self, team1, team2):
    return random.random()

  def fit_one_match(self, team1: Team, team2: Team, outcome: Outcome):
    pass
  
  def aquisition_function(self, team1, team2):
    # No preference for any match
    return 0.5
  
  @property
  def name(self):
    return "RandomEmulator"
