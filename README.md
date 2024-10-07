# skillbench

A multi-fidelity analysis of skill rating systems against CS:GO games! You can read our final report [here](https://arxiv.org/abs/2410.02831). This project was for the research component of Neil Lawrence's _Machine Learning and the Physical World_ ([L48](https://mlatcl.github.io/mlphysical/)) course. 

> **Abstract** — The meteoric rise of online games has created a
need for accurate skill rating systems, which can quickly
determine a team’s skill for the purpose of tracking
improvement and fair matchmaking. Although many systems
for determining skill ratings are deployed, with various
theoretical foundations, less work has been done at analysing
the real-world performance of these algorithms. In this
paper, we perform an empirical analysis of several systems
through the lens of surrogate modelling, where the model
can choose which matches are played next. We look both
at overall performance and data efficiency, and perform a
thorough sensitivity analysis.



## Installation

`pip install -e .` will install an editable version of Skillbench from the sources here, and install any required dependencies

Optional: first make a new virtualenv
```
conda create -n venv
conda activate venv
```

*Tested on Python 3.9.15.*

## Related Papers

#### Introduces rating system
- 🎁 [Example of the Glicko-2 system](http://www.glicko.net/glicko/glicko2.pdf) (2022)
  - n.b. Glicko-2 was first described in [2001](http://www.glicko.net/research/dpcmsv.pdf)
- 🎁 [TrueSkill 2: An improved Bayesian skill rating system](https://www.microsoft.com/en-us/research/uploads/prod/2018/03/trueskill2.pdf) (2018)
#### Introduces result predicter (beyond rating-based)
- 🏆 [Predicting Round Result in Counter-Strike: Global
Offensive Using Machine Learning](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9778597) (2022)
  - "Do ML models predict wins more accurately when we extend dataset to include Trueskill ratings?" -> Yes, slightly.
- 🏆 [Predicting the outcome of CS:GO
games using machine learning](https://publications.lib.chalmers.se/records/fulltext/256129/256129.pdf) (2018)
  - Used 50+ features, including weapon type and location of kills, to cluster players based on playstyle. Aim was to identify good team compositions.
  - Predicted match result based on *per-player cluster membership*:
    - Feed-forward NN: achieved `65.11%` accuracy
    - Winrate per cluster: achieved `58.97%` accuracy
      - Similar to our per-team WinRateEmulator achieving `~58.2%`
  - Data scraped from FACEIT as JSONs
#### Evaluates rating system
- 🔎 [The Evaluation of Rating Systems
in Online Free-for-All Games](https://arxiv.org/pdf/2008.06787.pdf) (2020)
- 🔎 [Predicting Winning Team and Probabilistic Ratings in “Dota 2” and “Counter-
Strike: Global Offensive” Video Games](https://drive.google.com/file/d/1MxVIfOb98fT19A1vmwoeyTuwxndUFxrv/view?usp=sharing) (2018)
  - From what I can tell: they use a novel model for Dota 2, but for CSGO just evaluate Trueskill?
  - Predicted match result based on *per-player Trueskill ratings*:
    - Trueskill: achieved `62%` accuracy on all data, `59%` on just dust2
