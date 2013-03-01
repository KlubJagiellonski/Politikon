def get_float_from_dict_or_fallback(dictionary, key, fallback):
    try:
        return float(dictionary.get(key, fallback))
    except ValueError:
        return fallback
    except TypeError:
        return fallback


def get_int_from_dict_or_fallback(dictionary, key, fallback):
    try:
        return int(dictionary.get(key, fallback))
    except ValueError:
        return fallback
    except TypeError:
        return fallback
