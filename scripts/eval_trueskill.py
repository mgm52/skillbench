from skillbench import Simulator, MatchDataset, download_matches
from skillbench.emulators import TrueSkillEmulator, RandomEmulator, WinRateEmulator
import matplotlib.pyplot as plt
import random
from skillbench.acquirers import TSAcquisitionFunction

### SETUP ###
# download_matches("data/matches.csv")
random.seed(0)
dataset = MatchDataset.from_csv("Dataset/csgo_34k.csv", random)
train_dataset, eval_dataset = dataset.split(0.9)

for mu in [10, 25, 40]:
    train_sim = Simulator(train_dataset, random)
    eval_sim = Simulator(eval_dataset, random)

    emu = TrueSkillEmulator(mu=mu, sigma=8.333)

    ### TRAIN ###
    n_evals = len(train_dataset)
    log_every = 2000

    t_accuracies = []
    e_accuracies = []
    logs = []
    for i in range(n_evals // log_every):
        train_sim.fit_emulator(emu, n_evals=log_every, acquisition_function=TSAcquisitionFunction(), max_aquisitions=100)

        t_accuracy = train_sim.evaluate_emulator(emu)
        t_accuracies.append(t_accuracy)
        print(f"Training accuracy {t_accuracy:.2%} at {(i+1) * log_every} matches")

        e_accuracy = eval_sim.evaluate_emulator(emu)
        e_accuracies.append(e_accuracy)
        print(f"Validation accuracy {e_accuracy:.2%} at {(i+1) * log_every} matches")

        logs.append((i+1) * log_every)

    ### VISUALIZE ###
    plt.plot(logs, e_accuracies, label=f"$\mu$={mu}")

plt.plot([0, n_evals], [0.5, 0.5], "k--")
plt.xlabel("Number of matches")
plt.ylabel("Validation accuracy")
plt.title(f"{emu.name}'s accuracy during training, with $\sigma$=8.333")
plt.legend()
plt.show()

eval_sim.evaluate_emulator(emu, visualize=True)
emu.visualize()