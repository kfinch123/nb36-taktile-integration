def add(data):
    """Function that summarized cols a and b"""

    data["sum"] = data["a"] + data["b"] + data["c"]

    return data


if __env:  # indicates we are running on Taktile
    data = add(data)
