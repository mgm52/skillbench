from skillbench import Simulator, MatchDataset, download_matches
from skillbench.emulators import TrueSkillEmulator

# download_matches("data/matches.csv")
dataset = MatchDataset.from_csv("Dataset/dataset1.csv")

train_dataset, eval_dataset = dataset.split(0.8)

train_sim = Simulator(train_dataset)
eval_sim = Simulator(eval_dataset)

emu = TrueSkillEmulator(mu=25, sigma=8.333)

train_sim.fit_emulator(emu, n_evals=300)
print(eval_sim.evaluate_emulator(emu))