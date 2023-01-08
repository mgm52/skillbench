from skillbench import emulators
from skillbench.acquirer import AcquisitionFunction, compatible_emulators
from skillbench.data import Team, TeamPair
from skillbench.emulator import Emulator
from skillbench import emulators
import random
import math

@compatible_emulators()
class MostSeenAF(AcquisitionFunction):
    def __call__(self, emu: Emulator, teams: TeamPair) -> float:
        super().__call__(emu, teams)
        team1, team2 = teams
        # One approach: assume that the more times a team has been seen, the more useful it will be to see it again, logarithmically
        if hasattr(emu, "player_fit_count"):
            counts = [emu.player_fit_count.get(player, 0) for player in team1.players + team2.players]
        else:
            counts = emu.team_fit_count.get(team1, 0), emu.team_fit_count.get(team2, 0)
        information = -1 * sum([math.log(count+1) for count in counts])
        return -1 * information

if __name__ == "__main__":
    lsaf = MostSeenAF()
    wr_emu = emulators.WinRateEmulator()
    print(lsaf.compatible_emulators)
    print(lsaf(wr_emu, TeamPair(Team("A"), Team("B"), random)))
    print(lsaf.name)
