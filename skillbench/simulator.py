import numpy as np
from collections import defaultdict
from tqdm import tqdm
from typing import Optional

from skillbench.emulator import Emulator
from skillbench.data import MatchDataset
from skillbench.acquirer import AcquisitionFunction
from skillbench import emulators 


class Simulator:
    def __init__(self, dataset: MatchDataset, random):
        self.dataset = dataset.copy()
        self.matchups_left = dict(self.dataset.matchups)
        self.random = random

    def reset_data(self):
        self.matchups_left = dict(self.dataset.matchups)

    def fit_emulator(self, emulator: Emulator, n_evals: int, acquisition_function: AcquisitionFunction, max_aquisitions: Optional[int] = None):        
        "Let the emulator choose N matches to learn from"
        bar = tqdm if n_evals > 10 else lambda x: x
        for i in bar(range(n_evals)):
            if len(self.matchups_left) == 0:
                print("Stopping training: no matches left")
                break

            # Let the emulator choose which match it wants to see next
            keys = self.matchups_left.keys()

            if max_aquisitions and len(keys) > max_aquisitions:
                keys = self.random.sample(list(keys), max_aquisitions)

            # TODO: validate that this order is random? i.e. to avoid bias among equal values
            top_matchup = max(keys, key=lambda k: acquisition_function(emulator, k))

            # When fitting a match, remove it from the dataset
            pop_id = self.random.choice(range(len(self.matchups_left[top_matchup])))
            winner = self.matchups_left[top_matchup].pop(pop_id).winner
            if len(self.matchups_left[top_matchup]) == 0:
                self.matchups_left.pop(top_matchup)

            emulator.fit_one_match(top_matchup, winner)

    def evaluate_emulator(self, emulator: Emulator, visualize=False, visualize_worst_matches=False):
        prediction_certainty_correct_match = []
        acc = []
        for match in self.dataset:
            if match.winner is not None:  # Don't evaluate draws
                # TODO: validate that this order is random
                team1, team2 = match.teams
                emu1 = emulator.emulate(team1, team2)
                emu2 = emulator.emulate(team2, team1)
                correct = (emu1 > emu2) == (match.winner == team1)
                acc.append(correct)
                if visualize:
                    prediction = f"{team1.name}>{team2.name}" if emu1 > emu2 else f"{team2.name}>{team1.name}"
                    certainty = abs(emu1 - emu2)
                    prediction_certainty_correct_match.append((prediction, certainty, correct, match))
        accuracy = np.mean(acc)

        if visualize:
            import matplotlib.pyplot as plt
            import matplotlib.font_manager as fm
            # Sort by certainty
            prediction_certainty_correct_match.sort(key=lambda x: x[1], reverse=True)
            limited = False
            limit = 100
            if len(prediction_certainty_correct_match) > limit:
                prediction_certainty_correct_match = prediction_certainty_correct_match[:limit]
                limited = True
            predictions = [x[0] for x in prediction_certainty_correct_match]

            # Workaround to allow multiple rows with same label
            positions = range(len(predictions))

            # Plot as a bar chart with color based on correct/incorrect
            plt.figure(figsize=(10, 10))
            plt.barh(
                positions,
                [x[1] for x in prediction_certainty_correct_match],
                color=["g" if x[2] else "r" for x in prediction_certainty_correct_match],
                label="_hid")

            # Workaround to add both colours to legend
            plt.scatter([], [], c="g", label="Correct")
            plt.scatter([], [], c="r", label="Incorrect")
            plt.legend(["Correct", "Incorrect"])

            plt.title(f"{emulator.name}'s predictions, {accuracy:.2%} accuracy" + (f", (limited to showing {limit} strongest predictions)" if limited else ""))
            plt.yticks(positions, predictions)
            plt.xlabel("Certainty (abs(team1winprob - team2winprob))")
            plt.ylabel("Prediction")
            plt.grid(axis="x")
            plt.show()
        
        if visualize_worst_matches:
            # Only works with TrueskillPlayersEmulator - hacky, sorry
            incorrect_matches = [x for x in prediction_certainty_correct_match if not x[2]]
            worst_matches = sorted(incorrect_matches, key=lambda x: x[1], reverse=True)
            if len(worst_matches) >= 3:
                for i in range(3):
                    pccm = worst_matches[i]
                    prediction, certainty, correct, match = pccm
                    team1, team2 = match.teams
                    winner = match.winner
                    emulator.visualize_match(team1, team2, winner, match_title=f"#{i+1} Worst match prediction.")

        return accuracy
