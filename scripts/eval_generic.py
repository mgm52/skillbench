import random
from skillbench import Simulator, MatchDataset, download_matches
from skillbench.emulators import TrueSkillEmulator, RandomEmulator, WinRateEmulator, StaticEmulator
import matplotlib.pyplot as plt
from skillbench.acquirers import LikeliestDrawAcquisitionFunction

### SETUP ###
# download_matches("data/matches.csv")

for seed in [0, 1, 2]:
    random.seed(seed)
    dataset = MatchDataset.from_csv("Dataset/csgo_34k.csv", random)

    train_dataset, eval_dataset = dataset.split(0.9)
    train_sim = Simulator(train_dataset, random)
    eval_sim = Simulator(eval_dataset, random)

    emu = WinRateEmulator()

    ### TRAIN ###
    print(f"Training {emu.name} with seed {seed}")
    n_evals = len(train_dataset)
    log_every = 2000

    t_accuracies = []
    e_accuracies = []
    logs = []
    for i in range(n_evals // log_every):
        train_sim.fit_emulator(emu, n_evals=log_every, acquisition_function=LikeliestDrawAcquisitionFunction(), max_aquisitions=100)

        t_accuracy = train_sim.evaluate_emulator(emu)
        t_accuracies.append(t_accuracy)
        print(f"Training accuracy {t_accuracy:.2%} at {(i+1) * log_every} matches")

        e_accuracy = eval_sim.evaluate_emulator(emu)
        e_accuracies.append(e_accuracy)
        print(f"Validation accuracy {e_accuracy:.2%} at {(i+1) * log_every} matches")

        logs.append((i+1) * log_every)

    ### VISUALIZE ###
    plt.plot(logs, e_accuracies, label=f"seed={seed}")

plt.plot([0, n_evals], [0.5, 0.5], "k--")
plt.xlabel("Number of matches")
plt.ylabel("Validation accuracy")
plt.title(f"{emu.name}'s accuracy during training")
plt.legend()
plt.show()

eval_sim.evaluate_emulator(emu, visualize=True)