# L48-true-skill-gp


## Installation

Tested on Python 3.9.7.

```
conda create -n venv
conda activate venv
pip install -r requirements.txt
```

---

## Ideas

### Data collection
- Source from HLTV
- Scrape using BeautifulSoup?

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
