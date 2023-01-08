from skillbench import emulators
from skillbench.acquirer import AcquisitionFunction, compatible_emulators
from skillbench.data import Team, TeamPair
from skillbench.emulator import Emulator
from skillbench import emulators
import random
import math
from math import pow

@compatible_emulators()
class CrossEntropyAF(AcquisitionFunction):

    def team_prob(self, emu: Emulator, team: Team):
        return (emu.team_fit_count.get(team, 0)+1) / (emu.team_fit_total+1)

    def __call__(self, emu: Emulator, teams: TeamPair) -> float:
        super().__call__(emu, teams)
        team1, team2 = teams
        
        pA = self.team_prob(emu, team1)
        pB = self.team_prob(emu, team2)
        pM = pA * pB

        pRA = max(emu.emulate(team1, team2), 0.001)
        pRB = max(emu.emulate(team2, team1), 0.001)

        return - pRA * math.log(pRA * pM) - pRB * math.log(pRB * pM)

if __name__ == "__main__":
    lsaf = CrossEntropyAF()
    wr_emu = emulators.WinRateEmulator()
    print(lsaf.compatible_emulators)
    print(lsaf(wr_emu, TeamPair(Team("A"), Team("B"), random)))
    print(lsaf.name)
