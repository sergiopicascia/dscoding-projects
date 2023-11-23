def convert_to_decimal(coord):
    if isinstance(coord, (float, int)):
        return coord

    direction_multipliers = {'N': 1, 'S': -1, 'E': 1, 'W': -1}
    for direction, multiplier in direction_multipliers.items():
        if direction in coord:
            return float(coord.strip(direction)) * multiplier

    return float(coord)

