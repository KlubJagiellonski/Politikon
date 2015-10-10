class Choices(object):
    """
    Provides an elegant way of defining a list of options consisting of
    a symbolic identifier, a value that can be stored in the database,
    a human-readable label and a dict of additional properties.
    """
    class Choice(object):
        name = None
        value = None
        label = None

        def __init__(self, name, value, label, extra={}):
            self.name = name
            self.value = value
            self.label = label
            for key, value in extra.iteritems():
                setattr(self, key, value)

    def __init__(self, *args):
        self._choices_source = args
        self._choices_dict = {}
        self._choices = []
        self._choices_twotuples = []
        for choice in self._choices_source:
            name, value, label = choice[:3]
            setattr(self, name, value)
            _choice = self.Choice(name, value, label) if len(choice) == 3 \
                else self.Choice(name, value, label, choice[3])
            setattr(self, '%s_CHOICE' % name, _choice)
            self._choices.append(_choice)
            self._choices_dict[value] = _choice
            self._choices_twotuples.append((value, label))

    def __getitem__(self, key):
        return self._choices_dict[key]

    def __iter__(self):
        return iter(self._choices_twotuples)
