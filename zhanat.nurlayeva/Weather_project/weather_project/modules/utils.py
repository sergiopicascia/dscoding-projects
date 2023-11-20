def convert_to_decimal(coord):
    """Convert a coordinate from string format to decimal format."""
    if isinstance(coord, (float, int)):
        return coord
    elif isinstance(coord, str):
        if 'W' in coord:
            return -float(coord.replace('W', ''))
        elif 'E' in coord:
            return float(coord.replace('E', ''))
        elif 'S' in coord:
            return -float(coord.replace('S', ''))
        elif 'N' in coord:
            return float(coord.replace('N', ''))
        else:
            return float(coord)
