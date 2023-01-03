import matplotlib.pyplot as plt
import pickle
import numpy as np

all_results = pickle.load(open("output/results.pkl", "rb"))

# 2 subplots for train and eval
fig, axs = plt.subplots(1, 2, figsize=(10, 10), sharey=True)

avg_train = []
min_train = []
max_train = []
avg_eval = []
min_eval = []
max_eval = []
std_train = []
std_eval = []
for name in all_results[0].keys():
    results = [r[name] for r in all_results]
    avg_train.append([sum(r[i][0] for r in results) / len(results) for i in range(len(results[0]))])
    min_train.append([min(r[i][0] for r in results) for i in range(len(results[0]))])
    max_train.append([max(r[i][0] for r in results) for i in range(len(results[0]))])
    std_train.append([np.std([r[i][0] for r in results]) for i in range(len(results[0]))])
    avg_eval.append([sum(r[i][1] for r in results) / len(results) for i in range(len(results[0]))])
    min_eval.append([min(r[i][1] for r in results) for i in range(len(results[0]))])
    max_eval.append([max(r[i][1] for r in results) for i in range(len(results[0]))])
    std_eval.append([np.std([r[i][1] for r in results]) for i in range(len(results[0]))])

for i, name in enumerate(all_results[0].keys()):
    axs[0].plot(avg_train[i], label=name)
    axs[0].fill_between(range(len(avg_train[i])), min_train[i], max_train[i], alpha=0.2)
    # axs[0].fill_between(range(len(avg_train[i])), np.array(avg_train[i]) - np.array(std_train[i]), np.array(avg_train[i]) + np.array(std_train[i]), alpha=0.2)
    axs[1].plot(avg_eval[i], label=name)
    axs[1].fill_between(range(len(avg_eval[i])), min_eval[i], max_eval[i], alpha=0.2)
    # axs[1].fill_between(range(len(avg_eval[i])), np.array(avg_eval[i]) - np.array(std_eval[i]), np.array(avg_eval[i]) + np.array(std_eval[i]), alpha=0.2)

axs[0].set_title("Train accuracy")
axs[1].set_title("Eval accuracy")
axs[0].legend()
axs[1].legend()
fig.suptitle("Accuracy during training (min, max, avg)")
plt.show()