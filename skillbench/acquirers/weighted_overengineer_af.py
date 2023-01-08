from skillbench import emulators
from skillbench.acquirer import AcquisitionFunction, compatible_emulators
from skillbench.data import Team, TeamPair
from skillbench.emulator import Emulator
from skillbench import emulators
import random
import math
from math import pow

@compatible_emulators()
class WeightedComplexAF(AcquisitionFunction):
    #   score = team_usefulness + universe_usefulness

    #   team_usefulness = iA*pA + iB*pB
    #   universe_usefulness = iA*pA*(1-pA) + iB*pB*(1-pB)

    #   overall, requirements for i1 calculation are:
    #      lower when uA higher    <- where uA is the understanding of A's skill
    #      higher when uB higher   <- means we have a more accurate understanding of B's skill to use as baseline for A's
    #      higher when draw prob higher    <-- doesnt make much sense for this to be entropy, because (if anything) it should spike at 0.5, not plateau
    #      lower when pM higher    <- note: we could switch from probs to counts - may even be better since it will maintain scale
    #   we use
    #   i1 = (1-|pR1-pR2|) + (uA+1 - uA)*uB + (1/cM)
    #       where uA = (1 - 1/cA)

    # So far best results obtained with WeightedComplexAF(0.5, -3.712, -7.265, 4, 0.472, 1.68, -0.111, -0.371)
    def __init__(self,
        draw_m: float = 1,       # draw factor                   multiplier
        draw_e: float = 1,       # draw factor                   exponent 
        newboost_m: float = 1,   # team's diminishing returns    multiplier 
        other_a: float = 1,      # other-team's usefulness       addition    0.3 <--any lower and matches between new teams would be the least useful
        matchup_m: float = 1,    # matchup's diminishing returns multiplier
        matchup_e: float = 1,    # matchup's diminishing returns exponent
        team_m: float = 1,       # team usefulness               multiplier 
        universe_m: float = 1    # universe usefulness           multiplier 
    ):
        super().__init__()
        self.draw_m = draw_m
        self.draw_e = draw_e
        self.newboost_m = newboost_m
        self.other_a = other_a
        self.matchup_m = matchup_m
        self.matchup_e = matchup_e
        self.team_m = team_m
        self.universe_m = universe_m

    # pA
    def team_prob(self, emu: Emulator, team: Team):
        return (emu.team_fit_count.get(team, 0)+1) / (emu.team_fit_total+1)

    # cA
    def team_count(self, emu, team: Team):
        return emu.team_fit_count.get(team, 0)+1

    # uA
    def understanding(self, count):
        return (1 - 1/count)

    def __call__(self, emu: Emulator, teams: TeamPair) -> float:
        super().__call__(emu, teams)
        team1, team2 = teams
        
        cA = self.team_count(emu, team1)
        cB = self.team_count(emu, team2)
        cM = emu.matchup_fit_count.get(teams, 0)+1

        pA = self.team_prob(emu, team1)
        pB = self.team_prob(emu, team2)

        pRA = emu.emulate(team1, team2)
        pRB = emu.emulate(team2, team1)

        uA = self.understanding(cA)
        uAnext = self.understanding(cA+1)
        uB = self.understanding(cB)
        uBnext = self.understanding(cB+1)

        draw_factor = max(1-abs(pRA-pRB), 0.001)
        matchup_factor = (1/cM)

        iA = self.draw_m*pow(draw_factor, self.draw_e) + self.newboost_m*(uAnext - uA)*(uB+self.other_a) + self.matchup_m*pow(matchup_factor, self.matchup_e)
        iB = self.draw_m*pow(draw_factor, self.draw_e) + self.newboost_m*(uBnext - uB)*(uA+self.other_a) + self.matchup_m*pow(matchup_factor, self.matchup_e)

        team_usefulness = iA*pA + iB*pB
        universe_usefulness = iA*pA*(1-pA) + iB*pB*(1-pB)

        return self.team_m * team_usefulness + self.universe_m * universe_usefulness

if __name__ == "__main__":
    lsaf = WeightedComplexAF()
    wr_emu = emulators.WinRateEmulator()
    print(lsaf.compatible_emulators)
    print(lsaf(wr_emu, TeamPair(Team("A"), Team("B"), random)))
    print(lsaf.name)
