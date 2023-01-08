from skillbench import emulators
from skillbench.acquirer import AcquisitionFunction, compatible_emulators
from skillbench.data import Team, TeamPair
from skillbench.emulator import Emulator
from skillbench import emulators
import random
import math
from math import pow

@compatible_emulators()
class WeightedAF(AcquisitionFunction):

    def __init__(self,
        draw_weight: float = 1,
        seen_weight: float = 1,
    ):
        super().__init__()
        self.draw_weight = draw_weight
        self.seen_weight = seen_weight

    def __call__(self, emu: Emulator, teams: TeamPair) -> float:
        super().__call__(emu, teams)
        team1, team2 = teams
        
        cA = emu.team_fit_count.get(team1, 0) + 1
        cB = emu.team_fit_count.get(team2, 0) + 1

        pRA = emu.emulate(team1, team2)
        pRB = emu.emulate(team2, team1)

        draw_factor = 1-abs(pRA-pRB)                            # linear slope from 1 to 0     (highest when draw)
        seen_factor = (1/cA - 1/(cA+1)) + (1/cB - 1/(cB+1))     # nonlinear slope from 1 to 0  (highest when unseen)

        return self.draw_weight * draw_factor + self.seen_weight * seen_factor

if __name__ == "__main__":
    lsaf = WeightedAF()
    wr_emu = emulators.WinRateEmulator()
    print(lsaf.compatible_emulators)
    print(lsaf(wr_emu, TeamPair(Team("A"), Team("B"), random)))
    print(lsaf.name)
