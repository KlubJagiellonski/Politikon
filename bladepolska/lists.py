from collections import defaultdict


def multilevel_group_by(iterable, groupers=[], getter=getattr):
    grouper = groupers.pop(0)

    result = defaultdict(list)
    for item in iterable:
        key = getter(item, grouper)

        result[key].append(item)

    if groupers:
        for key, value in result.iteritems():
            result[key] = multilevel_group_by(value, groupers, getter)

    return result
