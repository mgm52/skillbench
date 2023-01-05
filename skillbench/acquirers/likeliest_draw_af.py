from skillbench import emulators
from skillbench.acquirer import AcquisitionFunction, compatible_emulators
from skillbench.data import Team, TeamPair
from skillbench.emulator import Emulator
import random

@compatible_emulators()
class LikeliestDrawAF(AcquisitionFunction):
    def __call__(self, emu: Emulator, teams: TeamPair) -> float:
        super().__call__(emu, teams)
        team1, team2 = teams
        
        #if not (emu.name in ["RandomEmulator", "StaticEmulator"]) and not (emu.emulate(team1, team2) == (1-emu.emulate(team2, team1))):
        #    print(f"WARNING --- Emulator expected to be symmetric - but {emu.emulate(team1, team2)} != {1-emu.emulate(team2, team1)} for {team1} vs {team2} in {emu}")
        
        win_prob_diff = abs(emu.emulate(team1, team2) - emu.emulate(team2, team1))
        return 1 - win_prob_diff
