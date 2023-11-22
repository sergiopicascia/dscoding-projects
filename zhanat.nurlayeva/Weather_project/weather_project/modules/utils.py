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


#def convert_to_decimal(coord):
    #if isinstance(coord, (float, int)):
        #return coord
    #elif isinstance(coord, str):
        #if 'W' in coord:
            #return -float(coord.replace('W', ''))
        #elif 'E' in coord:
            #return float(coord.replace('E', ''))
        #elif 'S' in coord:
            #return -float(coord.replace('S', ''))
        #elif 'N' in coord:
            #return float(coord.replace('N', ''))
        #else:
            #return float(coord)


    #def convert_to_decimal(coord):
    """Convert a coordinate from string format to decimal format."""
    #if isinstance(coord, (float, int)):
        #return coord
    #elif isinstance(coord, str):
        #if 'W' in coord:
            #return -float(coord.replace('W', ''))
        #elif 'E' in coord:
            #return float(coord.replace('E', ''))
        #elif 'S' in coord:
            #return -float(coord.replace('S', ''))
        #elif 'N' in coord:
            #return float(coord.replace('N', ''))
        #else:
            #return float(coord)
