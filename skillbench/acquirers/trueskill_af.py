from skillbench.acquirer import AcquisitionFunction, compatible_emulators
from skillbench.data import Team, TeamPair
from skillbench.emulator import Emulator
from skillbench import emulators
import random

@compatible_emulators(emulators.TrueSkillEmulator, emulators.TrueSkillPlayersEmulator)
class TSQualityAF(AcquisitionFunction):
    def __call__(self, emu: Emulator, teams: TeamPair) -> float:
        super().__call__(emu, teams)
        # Get match quality from ts
        team1, team2 = teams
        if isinstance(emu, emulators.TrueSkillPlayersEmulator):
            rg1 = {player: rating for player, rating in zip(team1.players, emu.get_player_ratings(team1))}
            rg2 = {player: rating for player, rating in zip(team2.players, emu.get_player_ratings(team2))}
        else:
            rg1 = (emu.ratings.get(team1, emu.ts.Rating()),)
            rg2 = (emu.ratings.get(team2, emu.ts.Rating()),)
        # NOTE: TODO: figure out how this (ts.quality) works - docs say it's draw probability but source code seems more complex!
        return emu.ts.quality([rg1, rg2])

if __name__ == "__main__":
    tsaf = TSQualityAF()
    ts_emu = emulators.TrueSkillEmulator()
    print(tsaf.compatible_emulators)
    print(tsaf(ts_emu, TeamPair(Team("A"), Team("B"), random)))
    print(tsaf.name)
