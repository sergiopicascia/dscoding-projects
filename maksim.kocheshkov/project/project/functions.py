

def convert_coord(coord):
    #splitting
    parts = coord[:-1], coord[-1]
    
    num_val = float(parts[0])
   
    # If it has 'W' or 'S' - switch the value to a negative one
    if parts[1] in ['W', 'S']:
        num_val = num_val * (-1)

    return num_val