"""
Module with helper functions and others
"""
def get_game_duration(game_start, game_end):
    """
    Calculates the game duration
    :param game_start: start of the game (datetime.datetime)
    :param game_end: end of the game (datetime.datetime)
    :return: game duration as a formatted string
    """
    time_delta = game_end - game_start
    full_seconds = time_delta.total_seconds()
    minutes = int(full_seconds // 60)
    seconds = int(full_seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def pick_color(value):
    """
    Chooses the color of the text on the tile
    :param value: value of the tile (int)
    :return: color of the tile (str)
    """
    if value == 1:
        return "#0000FF"
    elif value == 2:
        return "#008000"
    elif value == 3:
        return "#FF0000"
    elif value == 4:
        return "#000080"
    elif value == 5:
        return "#800000"
    elif value == 6:
        return "#008080"
    elif value == 7:
        return "#808080"
    elif value == 8:
        return "#800080"
    else:
        return "#000000"
