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
    # iterate through each unit list:
    for unit in unitlist:
        # check if any value for a square in the list is equal to any other value
        # make a list of values in the squares
        val_list = [values[square] for square in unit]

        # find all duplicate values in that list that could be naked twins
        # criteria are 1) the number appears exactly twice in val_list and
        # 2) the number is 2 digits long
        nt_dupes_index = [i for i in range(0, len(val_list)) if
                    val_list.count(val_list[i]) == 2  and len(val_list[i]) == 2]

        # if there is at least one pair of naked twins
        if len(nt_dupes_index) == 2:
            # create a variable for the nt value
            nt_value = val_list[nt_dupes_index[0]]
            # turn the two values into a list
            nt_list_values = list(val_list[nt_dupes_index[0]])
            # iterate through the val_list to find common digits
            idx = 0
            for v in val_list:
                if len(v) > 1 and v != nt_value:
                    v_list = list(v)
                    found_nt_vals = [j for j in v_list if j in nt_list_values]
                    # if nt numbers found in value, replace it in the values dict
                    if len(found_nt_vals) > 0:
                        for k in found_nt_vals:
                            values[unit[idx]] = values[unit[idx]].replace(k, "")
                idx += 1


        # no naked twin pairs found
        else:
            continue
        #
        # nt_dupe_vals = [v_list[k] if k in nt_dupes_index]
        # print(nt_dupe_vals)
        #
        # # continue if there are duplicate values in the v_dupes list
        # if len(nt_dupes_index) > 0:
        #     no_nt_list = v_list[:]
        #     # make lists of vales in nt_exclude boxes to check
        #     non_nt_index = [n for n in range(len(v_list)) if n not in nt_dupes_index]
        #
        #     for j in non_nt_index:
        #         vals = list(v_list[j])
        #         if len(vals) > 1:
        #
        #     # if len(sq_not_nt_vals) > 1:
        #     #     for s in range(len(sq_not_nt_vals)):
        #     #         sqv = list(sq_not_nt_vals[s])
        #     #         for q in sqv:
        #     #             if q in nt_search:
        #     #                 # create a new variable with the nt value removed
        #     #                 new_sqv = sqv.remove(q)
        #     #                 # reassign the value of the square in the values dict
        #     #                 values[sq_not_nt[s]] = new_sqv
        #

    return (values)



naked_twins(values)


# for i in range(len(nt_exclude)):
#     square = nt_exclude[i]
#     square_values = list(values[square])
#     print("sq val", square_values)
#     for f in found_nt:
#         for fi in f:
#             if fi in square_values and len(square_values) > 1:
#                 square_values.remove(fi)
#                 print("removed", fi)
#                 values[square] = square_values
#             else:
#                 values[square] = square_values[0]
