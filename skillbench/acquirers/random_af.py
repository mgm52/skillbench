from skillbench import emulators
from skillbench.acquirer import AcquisitionFunction, compatible_emulators
from skillbench.data import Team, TeamPair
from skillbench.emulator import Emulator
import random

@compatible_emulators()
class RandomAF(AcquisitionFunction):
    def __call__(self, emu: Emulator, teams: TeamPair) -> float:
        super().__call__(emu, teams)
        return 0.5

if __name__ == "__main__":
    raf = RandomAF()
    rand_emu = emulators.RandomEmulator(random)
    print(raf.compatible_emulators)
    print(raf(rand_emu, TeamPair(Team("A"), Team("B"), random)))
    print(raf.name)
