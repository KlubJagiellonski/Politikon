'''
Elo calculations for multiplayer game

Based off https://github.com/FigBug/Multiplayer-ELO
'''
import math


class EloPlayer:
    def __init__(self):
        self.idx = None
        self.place = 0
        self.elo_pre = 0
        self.elo_post = 0
        self.elo_change = 0


class EloMatch:
    def __init__(self):
        self.players = []

    def add_player(self, idx, place, elo):
        player = EloPlayer()

        player.idx = idx
        player.place = place
        player.elo_pre = elo

        self.players.append(player)

    def get_elo(self, idx):
        try:
            return next(
                player.elo_post for player in self.players
                if player.idx == idx
            )
        except StopIteration:
            return 1400

    def get_elo_change(self, idx):
        try:
            return next(
                player.elo_change for player in self.players
                if player.idx == idx
            )
        except StopIteration:
            return 0

    def calculate_elos(self):
        k_factor = 32.0 / (len(self.players) - 1)

        for player in self.players:
            cur_place = player.place
            cur_elo = player.elo_pre

            opponents = list(self.players)
            opponents.remove(player)

            for opponent in opponents:
                opponent_place = opponent.place
                opponent_elo = opponent.elo_pre

                # Work out S
                if cur_place < opponent_place:
                    scored = 1.0
                elif cur_place == opponent_place:
                    scored = 0.5
                else:
                    scored = 0.0

                # Work out EA
                expected_a = 1 / (
                    1.0 + math.pow(10.0, (opponent_elo - cur_elo) / 400.0)
                )

                # Calculate ELO change vs this one opponent
                # I currently round at this point, this keeps rounding
                # changes symetrical between EA (expected_a) and EB,
                # but changes k_factor more than it should
                player.elo_change += round(k_factor * (scored - expected_a))

            # Add accumulated change to initial ELO for final ELO
            player.elo_post = player.elo_pre + player.elo_change
