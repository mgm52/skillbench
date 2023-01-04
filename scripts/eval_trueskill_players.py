import random
from skillbench import Simulator, MatchDataset
from skillbench.emulators import TrueSkillPlayersEmulator
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import defaultdict
from skillbench.acquirers import LikeliestDrawAcquisitionFunction

import argparse

def run_seed(seed):
    random.seed(seed)

    emus = [TrueSkillPlayersEmulator()]
    # dataset = MatchDataset.from_csv("Dataset/csgo_34k.csv", random)
    dataset = MatchDataset.from_json("Dataset/dataset4.json", random)

    #dataset = dataset.split(0.1, random=False)[0]
    train_dataset, eval_dataset = dataset.split(0.5, random=True)

    train_sims = [Simulator(train_dataset, random) for _ in emus]
    eval_sim = Simulator(eval_dataset, random)

    print(f"Training emulators {emus} with seed {seed}")

    seed_results = defaultdict(list)
    log_every = 500
    max_aquisitions = 25
    logs = []
    for i in tqdm(range(len(train_dataset))):
        for train_sim, emu in zip(train_sims, emus):
            train_sim.fit_emulator(emu, n_evals=1, acquisition_function=LikeliestDrawAcquisitionFunction(), max_aquisitions=max_aquisitions)

            if i % log_every == 0:
                acc_train = train_sim.evaluate_emulator(emu)
                acc_eval = eval_sim.evaluate_emulator(emu)

                print(f'{emu.name} accuracy: {acc_train:.2%} (train) {acc_eval:.2%} (eval) at {i} matches')
                seed_results[emu.name].append((acc_train, acc_eval))

        if i % log_every == 0:
            logs.append(i)

    # Visualize accuracy over time
    for emu_name, results in seed_results.items():
        plt.plot(logs, [r[0] for r in results], label=f"{emu_name} (train)")
        plt.plot(logs, [r[1] for r in results], label=f"{emu_name} (eval)")

    plt.legend()
    plt.xlabel("Number of matches")
    plt.ylabel("Accuracy")
    plt.title(f"Accuracy over time for seed {seed}")
    plt.show()

    emu = emus[0]
    #emu.visualize()
    eval_sim.evaluate_emulator(emu, visualize=True, visualize_worst_matches=True)

    return seed_results

if __name__ == '__main__':
    # run_seed(0)
    all_results = run_seed(0)
