from skillbench import Simulator, MatchDataset, download_matches
from skillbench.emulators import WinRateEmulator
import matplotlib.pyplot as plt

### SETUP ###
# download_matches("data/matches.csv")
dataset = MatchDataset.from_csv("Dataset/dataset1.csv")

train_dataset, eval_dataset = dataset.split(0.8)

train_sim = Simulator(train_dataset)
eval_sim = Simulator(eval_dataset)

emu = WinRateEmulator()

### TRAIN ###
n_evals = len(train_dataset)
log_every = 20

accuracies = [eval_sim.evaluate_emulator(emu)]
for i in range(n_evals // log_every):
    train_sim.fit_emulator(emu, n_evals=log_every)
    accuracy = eval_sim.evaluate_emulator(emu)
    accuracies.append(accuracy)
    print(f"Accuracy {accuracy:.2%} at {(i+1) * log_every} matches")

### VISUALIZE ###
plt.plot(range(0, n_evals+log_every, log_every), accuracies)

plt.plot([0, n_evals], [0.5, 0.5], "k--")
plt.xlabel("Number of matches")
plt.ylabel("Validation accuracy")
plt.title(f"{emu.name}'s accuracy during training")
plt.legend()
plt.show()

eval_sim.evaluate_emulator(emu, visualize=True)
emu.visualize()