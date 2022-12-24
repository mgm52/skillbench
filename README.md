# L48-true-skill-gp


## Installation

`pip install -e .` will install an editable version of Skillbench from the sources here, and install any required dependencies

Optional: first make a new virtualenv
```
conda create -n venv
conda activate venv
```

Tested on Python 3.9.15.
---

## Papers
### Rating systems
- [TrueSkill 2: An improved Bayesian skill rating system](https://www.microsoft.com/en-us/research/uploads/prod/2018/03/trueskill2.pdf)
  - 2018
- [Example of the Glicko-2 system](http://www.glicko.net/glicko/glicko2.pdf)
  - 2022
  - n.b. Glicko-2 was first described in [2001](http://www.glicko.net/research/dpcmsv.pdf)

### Evaluation of rating systems
- [The Evaluation of Rating Systems
in Online Free-for-All Games](https://arxiv.org/pdf/2008.06787.pdf)
  - 2020

## Ideas

### Data collection
- Source from HLTV - sadly no official api exists
- Scrape using BeautifulSoup

### Emulator
- GP mapping from (team, team) to (win probability) ??
- Implement TrueSkill & Glicko for comparison

### Simulator
- Decide on an acquisition function???

---

## Unknowns
- Do we model skill on a per-player basis or a per-team basis?
  - If per-team: how do we handle changing rosters?
- Implementation of all the TODOs :)
