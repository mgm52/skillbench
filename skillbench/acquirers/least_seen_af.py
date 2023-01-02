from skillbench import emulators
from skillbench.acquirer import AcquisitionFunction, compatible_emulators
from skillbench.data import Team, TeamPair
from skillbench.emulator import Emulator
from skillbench import emulators
import random

@compatible_emulators(emulators.WinRateEmulator)
class LeastSeenAcquisitionFunction(AcquisitionFunction):
    def __call__(self, emu: Emulator, teams: TeamPair) -> float:
        super().__call__(emu, teams)
        # Preference for smaller totals
        team1, team2 = teams
        return emu.maxtotal - (emu.matches_seen.get(team1, 0) + emu.matches_seen.get(team2, 0))

if __name__ == "__main__":
    lsaf = LeastSeenAcquisitionFunction()
    wr_emu = emulators.WinRateEmulator()
    print(lsaf.compatible_emulators)
    print(lsaf(wr_emu, TeamPair(Team("A"), Team("B"), random)))
    print(lsaf.name)
