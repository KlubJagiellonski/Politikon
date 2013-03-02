class NonexistantEvent(Exception):
    pass


class PriceMismatch(Exception):
    def __init__(self, message, updated_event):
        super(PriceMismatch, self).__init__(message)

        self.updated_event = updated_event


class EventNotInProgress(Exception):
    pass


class UnknownOutcome(Exception):
    pass


class InsufficientCash(Exception):
    def __init__(self, message, updated_user):
        super(PriceMismatch, self).__init__(message)

        self.updated_user = updated_user


class InsufficientBets(Exception):
    def __init__(self, message, updated_bet):
        super(PriceMismatch, self).__init__(message)

        self.updated_bet = updated_bet
