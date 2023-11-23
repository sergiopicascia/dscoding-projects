# utils.py

def convert_to_decimal(coord):
    if isinstance(coord, (float, int)):
        return coord
    elif isinstance(coord, str):
        try:
            # Remove any non-numeric characters from the coordinate string
            cleaned_coord = ''.join(char for char in coord if char.isdigit() or char in ['.', '-'])
            result = float(cleaned_coord) if cleaned_coord else None
            return result
        except ValueError as e:
            print(f"Error converting coordinate '{coord}': {e}")
            return None
    else:
        return None




