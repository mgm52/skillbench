import itertools
import numpy as np
import random
from tqdm import tqdm

from skillbench import MatchDataset, Simulator
from skillbench.emulators import Glicko2Emulator,TrueSkillEmulator, RandomEmulator, WinRateEmulator, StaticEmulator, EloEmulator, TrueSkillPlayersEmulator
from skillbench.acquirers import LikeliestDrawAcquisitionFunction

def logspace(start, end, num):
    return np.logspace(np.log10(start), np.log10(end), num)

params1 = {
    "mu": [25],
    "sigma": np.logspace(np.log10(25/3/10), np.log10(25/3*10), 40),
    "beta": np.logspace(np.log10(25/6/10), np.log10(25/6*10), 40),
    "tau": [25/300]
}

params2 = {
    "mu": [25],
    "sigma": [25/3],
    "beta": np.logspace(np.log10(25/6/10), np.log10(25/6*10), 40),
    "tau": np.logspace(np.log10(25/300/10), np.log10(25/300*10), 40)
}

params3 = {
    "mu": [25],
    "sigma": np.logspace(np.log10(25/3/10), np.log10(25/3*10), 40),
    "beta": [25/6],
    "tau": np.logspace(np.log10(25/300/10), np.log10(25/300*10), 40)
}

dataset = MatchDataset.from_json("Dataset/dataset4.json", random)
train_dataset, eval_dataset = dataset.split(0.5, random=52)

def search_run(params):
    random.seed(0)    

    try:
        emu = TrueSkillEmulator(**params)
        train_sim = Simulator(train_dataset, random)
        eval_sim = Simulator(eval_dataset, random)

        train_sim.fit_emulator(emu, n_evals=2000, acquisition_function=LikeliestDrawAcquisitionFunction(), max_aquisitions=25, bar=False)

        acc_eval = eval_sim.evaluate_emulator(emu)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(e)
        return [params, None]


    return [params, acc_eval]

def pool_run(pool, params):
    runs = list(itertools.product(*params.values()))
    # turn back into dicts
    runs = [dict(zip(params.keys(), run)) for run in runs]
    print(f"Running {len(list(runs))} runs")
    results = []
    # print(list(runs))
    for result in tqdm(pool.imap_unordered(search_run, list(runs)), total=len(runs)):
        results.append(result)

    return results

if __name__ == '__main__':
    import multiprocessing

    pool = multiprocessing.Pool(40)

    results1 = pool_run(pool, params1)
    results2 = pool_run(pool, params2)
    results3 = pool_run(pool, params3)

    pool.close()

    import pickle
    with open("output/ts_search1.pkl", "wb") as f:
        pickle.dump(results1, f)

    with open("output/ts_search2.pkl", "wb") as f:
        pickle.dump(results2, f)

    with open("output/ts_search3.pkl", "wb") as f:
        pickle.dump(results3, f)