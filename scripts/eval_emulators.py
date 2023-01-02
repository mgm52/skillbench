import random
from skillbench import Simulator, MatchDataset, download_matches
from skillbench.emulators import TrueSkillEmulator, RandomEmulator, WinRateEmulator, StaticEmulator, EloEmulator
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import defaultdict
import multiprocessing, pickle
from skillbench.acquirers import LikeliestDrawAcquisitionFunction

def run_seed(seed):
    random.seed(seed)

    emus = [StaticEmulator(), RandomEmulator(random), WinRateEmulator(), EloEmulator(), TrueSkillEmulator(), TrueSkillEmulator(acquisition="ts")]
    # dataset = MatchDataset.from_csv("Dataset/csgo_34k.csv", random)
    dataset = MatchDataset.from_json("Dataset/dataset3.json", random)

    train_dataset, eval_dataset = dataset.split(0.8)

    train_sims = [Simulator(train_dataset, random) for _ in emus]
    eval_sim = Simulator(eval_dataset, random)

    print(f"Training emulators {emus} with seed {seed}")

    # emus = [emulator() for emulator in emulators]

    seed_results = defaultdict(list)
    log_every = 100
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

    return seed_results

if __name__ == '__main__':
    # run_seed(0)
    pool = multiprocessing.Pool(8)
    all_results = pool.map(run_seed, range(8))

    with open("output/results.pkl", "wb") as f:
        pickle.dump(all_results, f)