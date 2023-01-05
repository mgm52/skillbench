from skillbench import emulators
from skillbench.acquirer import AcquisitionFunction, compatible_emulators
from skillbench.data import Team, TeamPair
from skillbench.emulator import Emulator
from skillbench import emulators
import random
import math

@compatible_emulators()
class LeastSeenPlayersAcquisitionFunction(AcquisitionFunction):
    def __call__(self, emu: Emulator, teams: TeamPair) -> float:
        super().__call__(emu, teams)
        team1, team2 = teams
        # One information-theoretic approach: assume that the more times a player has been seen, the more information we have about em, logarithmically
        counts = [emu.player_fit_count.get(player, 0) for player in team1.players + team2.players]
        information = -1 * sum([math.log(count+1) for count in counts])
        return information

if __name__ == "__main__":
    lsaf = LeastSeenPlayersAcquisitionFunction()
    wr_emu = emulators.WinRateEmulator()
    print(lsaf.compatible_emulators)
    print(lsaf(wr_emu, TeamPair(Team("A", ["a", "aa"]), Team("B", ["b", "bb"]), random)))
    print(lsaf.name)
