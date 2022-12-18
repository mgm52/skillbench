import random
import sklearn.metrics
import numpy as np
from collections import defaultdict

from skillbench.emulator import Emulator
from skillbench.data import MatchDataset, Outcome

class Simulator:
  def __init__(self, dataset: MatchDataset):
    self.matchups_all = defaultdict(list)
    self.dataset = dataset
    for match in dataset.matches:
      self.matchups_all[(match.team1, match.team2)].append(match.outcome)
      self.matchups_all[(match.team2, match.team1)].append(match.outcome)
    self.matchups_left = self.matchups_all.copy()

  def fit_emulator(self, emulator: Emulator, n_evals: int):
    "Let the emulator choose N matches to learn from"
    for i in range(n_evals):
      # Let the emulator choose which match it wants to see next
      keys = self.matchups_left.keys()
      
      top_matchup = max(keys, key=lambda k: emulator.aquisition_function(*k))
      
      # When fitting a match, remove it from the dataset
      pop_id = random.choice(range(len(self.matchups_left[top_matchup])))
      outcome = self.matchups_left[top_matchup].pop(pop_id)
      if len(self.matchups_left[top_matchup]) == 0:
        self.matchups_left.pop(top_matchup)
      
      emulator.fit_one_match(*top_matchup, outcome)

  def evaluate_emulator(self, emulator: Emulator):
    outcomes = []
    emulated_outcomes = []
    acc = []
    for match in self.dataset:
      if match.outcome != Outcome.DRAW: # Don't evaluate draws
        # outcomes.append(match.outcome == Outcome.TEAM1)
        # outcomes.extend([1, 0])
        emu1 = emulator.emulate(match.team1, match.team2)
        emu2 = emulator.emulate(match.team2, match.team1)
        acc.append(emu1 > emu2)

    print(np.mean(acc))

    # print(outcomes, emulated_outcomes)
    # return sklearn.metrics.log_loss(outcomes, emulated_outcomes)