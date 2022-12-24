from skillbench import Simulator, MatchDataset, download_matches
from skillbench.emulators import TrueSkillEmulator, RandomEmulator, WinRateEmulator
import matplotlib.pyplot as plt

# download_matches("data/matches.csv")
dataset = MatchDataset.from_csv("Dataset/csgo_34k.csv")

for split in [0.6, 0.7, 0.8, 0.9]:
    print(f"\nSplit: {split}")
    train_dataset, eval_dataset = dataset.split(split)

    # Compute how many of eval's matchups were seen in training,
    # & how much agreement there was with the outcomes seen.
    agreements = []
    for i in range(len(eval_dataset.matches)):
        em = eval_dataset.matches[i]
        seen_outcomes = train_dataset.matchups.get(em.teams) or []

        if len(seen_outcomes) > 0:
            # We saw this matchup in training, at least once!
            # Note: agreement would improve by about 1% if we factor in draws too.
            agrees = sum(1 for m in seen_outcomes if m.winner == em.winner)
            agreements.append(agrees / len(seen_outcomes))

    print(f"Average agreement with matching matchups: {sum(agreements) / len(agreements):.4g}")
    print(f"Proportion of eval matches seen in training: {len(agreements) / len(eval_dataset.matches):.4g}")