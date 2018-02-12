
from utils import *

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
    return (values)



def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    single_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in single_values:
        for p in peers[box]:
            values[p] = values[p].replace(values[box], '')

    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    for u in unitlist: # go through units (list of boxes)
        for d in '123456789': # look through each digit in the list
            dpl = [box for box in u if d in values[box]] # for each digit, make a list of boxes that has digit
            if len(dpl) == 1: # if the length of the list of boxes w a digit is 1
                values[dpl[0]] = d  # change the value of the box to that digit

    return values
    # raise NotImplementedError


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        eliminate(values)
        # Your code here: Use the Only Choice Strategy
        only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    # raise NotImplementedError


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
        # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        return False
    # check if it's solved e.g. length of all values in boxes is 1
    if all(len(values[b]) == 1 for b in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    v_len, box = min((len(values[s]), s) for s in boxes if len(values[s]) > 1) #tuple with len + box id
    # # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[box]:
        new_sudoku = values.copy() # copy the puzzle
        new_sudoku[box] = value # value is
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    # raise NotImplementedError


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.

        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    naked_twins(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
