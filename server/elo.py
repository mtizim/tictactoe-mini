from typing import Tuple
from tinydb import Query
import auth
import database as db


DEFAULT_ELO = 1500

__K = 15
__G = 1


def get_elo_for_token(token: str) -> int:
    player = auth.get_player_for_token(token)
    if player is None:
        return DEFAULT_ELO
    return player.leaderboard_data.elo


def update_elo(
    winner_token: str, loser_token: str
) -> Tuple[float, float]:  # Tuple contains winner and loser delta elo
    winner_elo = get_elo_for_token(winner_token)
    loser_elo = get_elo_for_token(loser_token)

    res = 1 / (10 ** ((loser_elo - winner_elo) / 400) + 1)

    delta_winner = (__K * __G) * (1 - res)
    delta_loser = -delta_winner

    winner_elo += delta_winner
    loser_elo += delta_loser

    __update_elo(winner_token, winner_elo, add_win=True)
    __update_elo(loser_token, loser_elo)

    return (delta_winner, delta_loser)


def __update_elo(token: str, new_elo: float, add_win=False):
    player = auth.get_player_for_token(token)
    if player is None:
        return

    player.leaderboard_data.elo = new_elo
    if add_win:
        player.leaderboard_data.wins = player.leaderboard_data.wins + 1

    player_q = Query()

    db.players.update(player.leaderboard_data, player_q.username == player.username)
