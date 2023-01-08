from skillbench import emulators
from skillbench.acquirer import AcquisitionFunction, compatible_emulators
from skillbench.data import MatchDataset, Team, TeamPair
from skillbench.emulator import Emulator
from skillbench import emulators
from trueskill import TrueSkill
import math
import copy
import random
from skillbench.simulator import Simulator

@compatible_emulators()
class CheatingAF(AcquisitionFunction):
    def __init__(self, random, max_evals_per_matchup=1):
        super().__init__()
        self.random = random
        self.max_evals_per_matchup = max_evals_per_matchup
    
    def load_sim(self, sim: Simulator):
        self.sim = sim

    def __call__(self, emu: Emulator, teams: TeamPair) -> float:
        super().__call__(emu, teams)

        possible_results = self.sim.matchups_left[teams].copy()
        accs = []
        for i in range(min(len(possible_results), self.max_evals_per_matchup)):
            outcome = possible_results.pop(self.random.randint(0, len(possible_results)-1))

            emu2 = copy.deepcopy(emu)
            emu2.fit_one_match(teams, outcome.winner)
            accs.append(self.sim.evaluate_emulator(emu2))

        return sum(accs) / len(accs)

if __name__ == "__main__":
    dataset = MatchDataset.from_json("Dataset/dataset4.json", random)
    train_ds, eval_ds = dataset.split(0.5, random=32)
    train_sim = Simulator(train_ds, random)

    chaf = CheatingAF(train_sim, random)
    wr_emu = emulators.TrueSkillEmulator()
    print(chaf.compatible_emulators)
    for i in range(len(train_sim.matchups_left.keys())):
        print(chaf(wr_emu, list(train_sim.matchups_left.keys())[i]))
    print(chaf.name)
