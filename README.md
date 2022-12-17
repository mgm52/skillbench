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
