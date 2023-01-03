from skillbench.acquirer import AcquisitionFunction, compatible_emulators
from skillbench.data import Team, TeamPair
from skillbench.emulator import Emulator
from skillbench import emulators
import random

@compatible_emulators(emulators.TrueSkillEmulator)
class TSAcquisitionFunction(AcquisitionFunction):
    def __call__(self, emu: Emulator, teams: TeamPair) -> float:
        super().__call__(emu, teams)
        # Get match quality from ts
        team1, team2 = teams
        rating1 = emu.ratings.get(team1, emu.ts.Rating())
        rating2 = emu.ratings.get(team2, emu.ts.Rating())
        # NOTE: TODO: figure out how this works - docs say it's draw probability but source code seems more complex!
        return emu.ts.quality([(rating1,), (rating2,)])

if __name__ == "__main__":
    tsaf = TSAcquisitionFunction()
    ts_emu = emulators.TrueSkillEmulator()
    print(tsaf.compatible_emulators)
    print(tsaf(ts_emu, TeamPair(Team("A"), Team("B"), random)))
    print(tsaf.name)
