import random
import numpy as np
from collections import defaultdict

from skillbench.emulator import Emulator
from skillbench.data import MatchDataset, Outcome, flip_outcome

class Simulator:
  def __init__(self, dataset: MatchDataset):
    # Flip the outcome for every other match in dataset
    self.dataset = dataset
    for i in range(len(dataset.matches)):
      if i % 2 == 1:
        dataset.matches[i].outcome = flip_outcome(dataset.matches[i].outcome)
        dataset.matches[i].team1, dataset.matches[i].team2 = dataset.matches[i].team2, dataset.matches[i].team1

    # Create a dictionary of all matchups and their outcomes
    self.matchups_all = defaultdict(list)
    for match in dataset.matches:
      self.matchups_all[(match.team1, match.team2)].append(match.outcome)
      self.matchups_all[(match.team2, match.team1)].append(flip_outcome(match.outcome))
    
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

  def evaluate_emulator(self, emulator: Emulator, visualize=False):
    prediction_certainty_correct = []
    acc = []
    for match in self.dataset:
      if match.outcome != Outcome.DRAW: # Don't evaluate draws
        # outcomes.append(match.outcome == Outcome.TEAM1)
        # outcomes.extend([1, 0])
        emu1 = emulator.emulate(match.team1, match.team2)
        emu2 = emulator.emulate(match.team2, match.team1)
        correct = (emu1 > emu2) == (match.outcome == Outcome.TEAM1)
        acc.append(correct)
        if visualize:
          prediction = f"{match.team1.name}>{match.team2.name}" if emu1 > emu2 else f"{match.team2.name}>{match.team1.name}"
          # Check whether prediction exists in prediction_certainty_correct already
          certainty = abs(emu1 - emu2)
          prediction_certainty_correct.append((prediction, certainty, correct))
    accuracy = np.mean(acc)

    if visualize:
      import matplotlib.pyplot as plt
      import matplotlib.font_manager as fm
      # Sort by certainty
      prediction_certainty_correct.sort(key=lambda x: x[1], reverse=True)
      predictions = [x[0] for x in prediction_certainty_correct]

      # Workaround to allow multiple rows with same label
      positions = range(len(predictions))

      # Plot as a bar chart with color based on correct/incorrect
      plt.figure(figsize=(10, 10))
      plt.barh(
        positions,
        [x[1] for x in prediction_certainty_correct],
        color=["g" if x[2] else "r" for x in prediction_certainty_correct],
        label="_hid")

      # Workaround to add both colours to legend
      plt.scatter([], [], c="g", label="Correct")
      plt.scatter([], [], c="r", label="Incorrect")
      plt.legend(["Correct", "Incorrect"])

      plt.title(f"{emulator.name}'s predictions, {accuracy:.2%} accuracy")
      plt.yticks(positions, predictions)
      plt.xlabel("Certainty")
      plt.ylabel("Prediction")
      plt.grid(axis="x")
      plt.show()

    return accuracy