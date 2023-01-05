from skillbench.emulator import Emulator
from trueskill import TrueSkill
import itertools
import math
import matplotlib.pyplot as plt

from skillbench.data import Team, TeamPair

# TODO: create acquisition function for Glicko2
####### Glicko2 class based on https://github.com/sublee/glicko2/blob/master/glicko2.py under BSD license
class Glicko2Emulator(Emulator):
    def __init__(self, mu=1500, phi=350, sigma=0.06, tau=1.0, epsilon=0.000001):
        super().__init__()
        self.mu = mu
        self.phi = phi
        self.sigma = sigma
        self.tau = tau
        self.epsilon = epsilon
        self.ratings = {}
    
    class Rating(object):
        def __init__(self, mu, phi, sigma):
            self.mu = mu
            self.phi = phi
            self.sigma = sigma

    def get_rating(self, team):
        return self.ratings.get(team, self.Rating(self.mu, self.phi, self.sigma))

    def emulate(self, team1, team2):
        r1 = self.get_rating(team1)
        r2 = self.get_rating(team2)

        impact = self.reduce_impact(r2)
        expected_score = self.expect_score(r1, r2, impact)
        # print(f"Expected score of team with rating {r1.mu} against {r2.mu}: {expected_score}\n")
        # assert 0 <= expected_score <= 1, "Expected score should be between 0 and 1"
        # assert (r1.mu < r2.mu) == (expected_score < 0.5), "Lower rating should have lower expected score"
        # assert (expected_score == 0.5) == (r1.mu == r2.mu), "Equal rating should have expected score of 0.5"
        return expected_score

    def fit_one_match(self, teams: TeamPair, winner: Team):
        super().fit_one_match(teams, winner)
        # Use outcome to update rating of each team (i.e. self.ratings)
        team1, team2 = teams
        if winner:
            loser = team1 if winner == team2 else team2
            self.rate(winner, [(1, loser)])
            self.rate(loser, [(0, winner)])
        else:
            self.rate(team1, [(0.5, team2)])
            self.rate(team2, [(0.5, team1)])

    def determine_sigma(self, rating, difference, variance):
        """Determines new sigma."""
        phi = rating.phi
        difference_squared = difference ** 2
        # 1. Let a = ln(s^2), and define f(x)
        alpha = math.log(rating.sigma ** 2)

        def f(x):
            """This function is twice the conditional log-posterior density of
            phi, and is the optimality criterion.
            """
            tmp = phi ** 2 + variance + math.exp(x)
            a = math.exp(x) * (difference_squared - tmp) / (2 * tmp ** 2)
            b = (x - alpha) / (self.tau ** 2)
            return a - b

        # 2. Set the initial values of the iterative algorithm.
        a = alpha
        if difference_squared > phi ** 2 + variance:
            b = math.log(difference_squared - phi ** 2 - variance)
        else:
            k = 1
            while f(alpha - k * math.sqrt(self.tau ** 2)) < 0:
                k += 1
            b = alpha - k * math.sqrt(self.tau ** 2)
        # 3. Let fA = f(A) and f(B) = f(B)
        f_a, f_b = f(a), f(b)
        # 4. While |B-A| > e, carry out the following steps.
        # (a) Let C = A + (A - B)fA / (fB-fA), and let fC = f(C).
        # (b) If fCfB < 0, then set A <- B and fA <- fB; otherwise, just set
        #     fA <- fA/2.
        # (c) Set B <- C and fB <- fC.
        # (d) Stop if |B-A| <= e. Repeat the above three steps otherwise.
        while abs(b - a) > self.epsilon:
            c = a + (a - b) * f_a / (f_b - f_a)
            f_c = f(c)
            if f_c * f_b < 0:
                a, f_a = b, f_b
            else:
                f_a /= 2
            b, f_b = c, f_c
        # 5. Once |B-A| <= e, set s' <- e^(A/2)
        return math.exp(1) ** (a / 2)

    def scale_down(self, rating, ratio=173.7178):
        mu = (rating.mu - self.mu) / ratio
        phi = rating.phi / ratio
        return self.Rating(mu, phi, rating.sigma)

    def scale_up(self, rating, ratio=173.7178):
        mu = rating.mu * ratio + self.mu
        phi = rating.phi * ratio
        return self.Rating(mu, phi, rating.sigma)

    def reduce_impact(self, rating):
        """The original form is `g(RD)`. This function reduces the impact of
        games as a function of an opponent's RD.
        """
        return 1. / math.sqrt(1 + (3 * rating.phi ** 2) / (math.pi ** 2))

    def expect_score(self, rating, other_rating, impact):
        return 1. / (1 + math.exp(-impact * (rating.mu - other_rating.mu)))

    def rate(self, team, result_and_other_team):
        # Step 2. For each player, convert the rating and RD's onto the
        #         Glicko-2 scale.
        rating = self.get_rating(team)
        rating = self.scale_down(rating)
        # Step 3. Compute the quantity v. This is the estimated variance of the
        #         team's/player's rating based only on game outcomes.
        # Step 4. Compute the quantity difference, the estimated improvement in
        #         rating by comparing the pre-period rating to the performance
        #         rating based only on game outcomes.
        variance_inv = 0
        difference = 0
        if not result_and_other_team:
            # If the team didn't play in the series, do only Step 6
            phi_star = math.sqrt(rating.phi ** 2 + rating.sigma ** 2)
            self.ratings[team] = self.scale_up(self.Rating(rating.mu, phi_star, rating.sigma))
            return self.ratings[team]
        for actual_score, other_team in result_and_other_team:
            other_rating = self.get_rating(other_team)
            other_rating = self.scale_down(other_rating)
            impact = self.reduce_impact(other_rating)
            expected_score = self.expect_score(rating, other_rating, impact)
            variance_inv += impact ** 2 * expected_score * (1 - expected_score)
            difference += impact * (actual_score - expected_score)
        difference /= variance_inv
        variance = 1. / variance_inv
        # Step 5. Determine the new value, Sigma', ot the sigma. This
        #         computation requires iteration.
        sigma = self.determine_sigma(rating, difference, variance)
        # Step 6. Update the rating deviation to the new pre-rating period
        #         value, Phi*.
        phi_star = math.sqrt(rating.phi ** 2 + sigma ** 2)
        # Step 7. Update the rating and RD to the new values, Mu' and Phi'.
        phi = 1. / math.sqrt(1 / phi_star ** 2 + 1 / variance)
        mu = rating.mu + phi ** 2 * (difference / variance)
        # Step 8. Convert ratings and RD's back to original scale.
        self.ratings[team] = self.scale_up(self.Rating(mu, phi, sigma))
        return self.ratings[team]

    @property
    def name(self):
        return "Glicko2({}, {}, {}, {}, {})".format(self.mu, self.phi, self.sigma, self.tau, self.epsilon)
