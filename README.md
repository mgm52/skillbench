# L48-true-skill-gp


## Installation

`pip install -e .` will install an editable version of Skillbench from the sources here, and install any required dependencies

Optional: first make a new virtualenv
```
conda create -n venv
conda activate venv
```

*Tested on Python 3.9.15.*

## Papers

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
    

## Ideas

### Data collection
- Source from HLTV - sadly no official api exists
- Scrape using BeautifulSoup

### Emulator
- GP mapping from (team, team) to (win probability) ??
- Implement TrueSkill & Glicko for comparison

### Simulator
- Decide on an acquisition function???

## Implementation references

Both: https://github.com/mbhynes/skelo [2 stars]

### Elo
- https://github.com/ddm7018/Elo/blob/master/elosports/elo.py [39 stars]
- https://github.com/sublee/elo/blob/master/elo.py [87 stars]
### Glicko2
- https://github.com/ryankirkman/pyglicko2 [22 stars]
- https://github.com/deepy/glicko2 [19 stars]
- https://github.com/sublee/glicko [15 stars, "DO NOT USE"]

---

## Unknowns
- Do we model skill on a per-player basis or a per-team basis?
  - If per-team: how do we handle changing rosters?
- Implementation of all the TODOs :)
