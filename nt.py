rows = 'ABCDEFGHI'
cols = '123456789'
boxes = [r + c for r in rows for c in cols]
def cross(A, B):
    """Cross product of elements in A and elements in B """
    return [x+y for x in A for y in B]
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
diagonal_lr = [rows[i] + cols[i] for i in range(len(rows))]
diagonal_rl = [rows[i] + cols[i] for i in range(len(rows) -1, -1, -1)]
unitlist.append(diagonal_rl)
unitlist.append(diagonal_lr)


units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

values = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
                        'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
                        'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
                        'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
                        'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
                        'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
                        'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
                        'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
                        'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
                        'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
                        'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}

def naked_twins(values):
    # find all two value boxes in the puzzle - potential naked twins pairs
    two_val_boxes = [box for box in values.keys() if len(values[box]) == 2]
    nt_dict = {k:[] for k in two_val_boxes}

    # fill in the values for peer boxes with the same values
    for box in nt_dict.keys():
        box_peers = list(peers[box]) # create a copy of the peers list
        # list peers that have 2 values
        box_p2 = [p for p in box_peers if values[p] == values[box]]
        # for each peer, check if the peer values are the same as the
        nt_dict[box] = box_p2
    print(nt_dict)
    # replace values in relevant row, col
    for k, v in nt_dict.items():
        if len(v) >= 1:
            if k[0] ==  v[0][0]:
                check_group = [k[0] + str(i) for i in cols]
            elif k[1] == v[0][1]:
                check_group = [str(i) + k[1]  for i in rows]
            else:
                check_group = [p for p in peers[k] if p[0] != k[0] and p[1] !=k[1]]
            if len(v) >= 1:
                vals = list(values[k])
                for p in peers[k]:
                    p_vals = list(values[p])
                    for i in vals:
                        if i in p_vals:
                            print((values[p]))
                            values[p].replace(i, '')

    return (values)



naked_twins(values)
