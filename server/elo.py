import auth

DEFAULT_ELO = 1500


def getEloForToken(token: str) -> int:
    player = auth.get_player_for_token(token)
    if player is None:
        return DEFAULT_ELO
    player.leaderboard_data.elo
