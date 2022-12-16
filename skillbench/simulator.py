import random
import sklearn.metrics

from skillbench.emulator import Emulator
from skillbench.data import MatchDataset

class Simulator:
  def __init__(self, dataset: MatchDataset):
    self.matchups_all = {}
    for match in dataset.matches:
      self.matchups_all[(match.team1, match.team2)].append(match.outcome)
      self.matchups_all[(match.team2, match.team1)].append(match.outcome)
    self.matchups_left = self.matchups_all.copy()

  def fit_emulator(self, emulator: Emulator, n_evals: int):
    "Let the emulator choose N matches to learn from"
    for i in range(n_evals):
      # Let the emulator choose which match it wants to see next
      keys = self.matchups_left.keys()
      
      top_matchup = max(keys, key=lambda t1, t2: emulator.aquisition_function(t1, t2))
      
      # When fitting a match, remove it from the dataset
      pop_id = random.choice(range(len(self.matchups_left(top_matchup))))
      outcome = self.matchups_left[top_matchup].pop(pop_id)
      if len(self.matchups_left[top_matchup]) == 0:
        self.matchups_left.pop(top_matchup)
      
      emulator.fit_one_match(*top_matchup, outcome)

  def evaluate_emulator(self, emulator: Emulator):
    outcomes = []
    emulated_outcomes = []
    for match in self.matchups_all:
      outcomes.append(match.outcome)
      emulated_outcomes.append(emulator.emulate(match))

    return sklearn.metrics.logloss(outcomes, emulated_outcomes)