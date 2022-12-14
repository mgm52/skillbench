from emulator import Emulator
from trueskill import TrueSkill

# An example emulator.
class TrueSkillEmulator(Emulator):
  def __init__(self, mu, sigma):
    self.ts = TrueSkill(mu, sigma)

  def emulate(self, team1, team2):
    return self.ts.win_probability(team1, team2)

  # ...