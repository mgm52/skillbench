from skillbench import emulators
from skillbench.acquirer import AcquisitionFunction, compatible_emulators
from skillbench.data import Team, TeamPair
from skillbench.emulator import Emulator
import random

@compatible_emulators()
class LikeliestWinAF(AcquisitionFunction):
    def __call__(self, emu: Emulator, teams: TeamPair) -> float:
        super().__call__(emu, teams)
        team1, team2 = teams
        win_prob_diff = abs(emu.emulate(team1, team2) - emu.emulate(team2, team1))
        return win_prob_diff