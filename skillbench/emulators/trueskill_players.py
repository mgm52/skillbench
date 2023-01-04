from skillbench.emulator import Emulator
from trueskill import TrueSkill
import itertools
import math
import matplotlib.pyplot as plt

from skillbench.data import Team, TeamPair


class TrueSkillPlayersEmulator(Emulator):
    def __init__(self, mu=25, sigma=25/3):
        self.mu = mu
        self.sigma = sigma
        self.ts = TrueSkill(mu, sigma)
        self.ratings = {}

    def get_player_ratings(self, team):
        return [self.ratings.get(player, self.ts.Rating()) for player in team.players]

    def emulate(self, team1, team2):
        # Replace teams by their rating
        team1 = self.get_player_ratings(team1)
        team2 = self.get_player_ratings(team2)

        # This function was written by Juho Snellman https://github.com/sublee/trueskill/issues/1#issuecomment-149762508
        delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
        sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
        size = len(team1) + len(team2)
        denom = math.sqrt(size * (self.ts.beta * self.ts.beta) + sum_sigma)
        return self.ts.cdf(delta_mu / denom)

    def fit_one_match(self, teams: TeamPair, winner: Team):
        # Use outcome to update rating of each team's players (i.e. self.ratings)
        team1, team2 = teams
        rg1 = {player: rating for player, rating in zip(team1.players, self.get_player_ratings(team1))}
        rg2 = {player: rating for player, rating in zip(team2.players, self.get_player_ratings(team2))}

        if winner == team1:
            new_ratings = self.ts.rate([rg1, rg2], ranks=[0, 1])
        elif winner == team2:
            new_ratings = self.ts.rate([rg1, rg2], ranks=[1, 0])
        else:
            new_ratings = self.ts.rate([rg1, rg2], ranks=[0, 0])
        # print(new_ratings)

        self.ratings.update(new_ratings[0])
        self.ratings.update(new_ratings[1])

    @property
    def name(self):
        return "TrueSkillPlayers({}, {})".format(self.mu, self.sigma)

    def visualize(self):
        players = list(self.ratings.keys())
        players.sort(key=lambda x: x.lower())
        mus = [self.ratings.get(player).mu for player in players]
        sigmas = [self.ratings.get(player).sigma for player in players]

        players = [player.replace("$", "\\$") for player in players]
        plt.errorbar(mus, players, xerr=sigmas, fmt='o')
        plt.axvline(x=self.ts.mu, color='r', linestyle='--')
        plt.title("TrueSkill ratings ($\mu \pm \sigma$)")
        plt.legend(["Initial avg rating", "Team rating $\mu \pm \sigma$"])
        plt.show()

    def visualize_match(self, team1, team2, winner, match_title=""):
        # On left subplot, plot team1's players' ratings
        # On right subplot, plot team2's players' ratings

        loser = team1 if winner == team2 else team2
        winner_advantage = self.emulate(winner, loser) - self.emulate(loser, winner)
        certainty = abs(winner_advantage)

        predicted_winner = winner if winner_advantage > 0 else loser

        team1_ratings = self.get_player_ratings(team1)
        team2_ratings = self.get_player_ratings(team2)

        # Plot team1's players' ratings
        plt.subplot(1, 2, 1)
        players = [player.replace("$", "\\$") for player in team1.players]
        mus = [rating.mu for rating in team1_ratings]
        sigmas = [rating.sigma for rating in team1_ratings]
        plt.errorbar(mus, players, xerr=sigmas, fmt='o')
        plt.axvline(x=self.ts.mu, color='r', linestyle='--')
        plt.title(f"Team {team1.name} ratings ($\mu \pm \sigma$)")
        plt.legend(["Initial avg rating", "Team rating $\mu \pm \sigma$"])

        # Plot team2's players' ratings
        plt.subplot(1, 2, 2)
        players = [player.replace("$", "\\$") for player in team2.players]
        mus = [rating.mu for rating in team2_ratings]
        sigmas = [rating.sigma for rating in team2_ratings]
        plt.errorbar(mus, players, xerr=sigmas, fmt='o')
        plt.axvline(x=self.ts.mu, color='r', linestyle='--')
        plt.title(f"Team {team2.name} ratings ($\mu \pm \sigma$)")
        plt.legend(["Initial avg rating", "Team rating $\mu \pm \sigma$"])

        # correct = "correct" if winner == team1 else "incorrect"
        title = "Team {} won. Trueskill emu thought {} would win, having positive certainty of {:.4f}.".format(winner.name, predicted_winner.name, certainty)
        if match_title: title = match_title + "\n" + title
        plt.suptitle(title)

        plt.show()
