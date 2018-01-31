class TeamJoiningError(Exception):
    """
    Base exception for errors related to joining a team
    """

class UserAlreadyPlayed(TeamJoiningError):
    """
    Exception indicating that user can't join a team because he already bought
    a bet
    """
    pass


class InvalidAccessKey(TeamJoiningError):
    """
    Error raised when accesskey is invalid
    """

