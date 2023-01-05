import itertools
import numpy as np
import random
from tqdm import tqdm

from skillbench import MatchDataset, Simulator
from skillbench.emulators import Glicko2Emulator,TrueSkillEmulator, RandomEmulator, WinRateEmulator, StaticEmulator, EloEmulator, TrueSkillPlayersEmulator
from skillbench.acquirers import LikeliestDrawAF, LeastSeenAF, RandomAF, LikeliestWinAF, TSQualityAF

def logspace(start, end, num):
    return np.logspace(np.log10(start), np.log10(end), num)

params = {
    "emu": [TrueSkillEmulator, TrueSkillPlayersEmulator, EloEmulator, Glicko2Emulator, WinRateEmulator, lambda: RandomEmulator(random)],
    "af": [LikeliestDrawAF, LeastSeenAF, RandomAF, LikeliestWinAF, TSQualityAF]
}

dataset = MatchDataset.from_json("Dataset/dataset4.json", random)
train_dataset, eval_dataset = dataset.split(0.5, random=52)

def search_run(params):
    random.seed(params['seed'])    

    emu = params["emu"]()
    af = params["af"]()

    train_sim = Simulator(train_dataset, random)
    eval_sim = Simulator(eval_dataset, random)

    train_results = []
    eval_results = []
    x = []
    try:
        log_every = 100
        max_aquisitions = 25
        logs = []
        for i in range(len(train_dataset)):
            train_sim.fit_emulator(emu, n_evals=1, acquisition_function=af, max_aquisitions=max_aquisitions)

            if i % log_every == 0:
                acc_train = train_sim.evaluate_emulator(emu)
                acc_eval = eval_sim.evaluate_emulator(emu)

                # print(f'{emu.name} accuracy: {acc_train:.2%} (train) {acc_eval:.2%} (eval) at {i} matches')
                # seed_results[emu.name].append((acc_train, acc_eval))
                train_results.append(acc_train)
                eval_results.append(acc_eval)
                x.append(i)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(e)
        return [params, None]


    return [params, x, train_results, eval_results]

# def pool_run(pool, params):
#     runs = list(itertools.product(*params.values()))
#     # turn back into dicts
#     runs = [dict(zip(params.keys(), run)) for run in runs]
#     print(f"Running {len(list(runs))} runs")
#     results = []
#     # print(list(runs))
#     for result in tqdm(pool.imap_unordered(search_run, list(runs)), total=len(runs)):
#         results.append(result)

#     return results

def pool_run(pool, params, n=1):
    # n is the number of times to repeat each run
    runs = list(itertools.product(*params.values()))
    runs = [dict(zip(params.keys(), run)) for run in runs]
    
    print(f"Running {len(list(runs))} runs")
    # Filter on emu/af compatibility
    runs = [run for run in runs if run['af']().compatible_with(run['emu']())]
    print(f"Running {len(list(runs))} runs after filtering")
    runs = [{**run, 'seed': i} for run in runs for i in range(n)]
    print(f"Running {len(list(runs))} runs with {pool._processes} cores")

    # execute
    results = []
    for result in tqdm(pool.imap_unordered(search_run, list(runs)), total=len(runs), smoothing=0.05):
        results.append(result)

    return results


if __name__ == '__main__':
    import multiprocessing

    pool = multiprocessing.Pool(1)
    results1 = pool_run(pool, params, 100)

    import pickle
    with open("output/large_search.pkl", "wb") as f:
        pickle.dump(results1, f)
