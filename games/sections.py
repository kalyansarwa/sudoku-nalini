""" This module returns various chunks of the grid """
import math


def get_horz(grid, square, unsolved=False):
    """ get row minus reference square """

    related = []

    for square2 in grid.grid[square.row]:
        if square2 != square:
            if not unsolved:
                related.append(square2)
            elif not square2.answer:
                related.append(square2)

    return related



def get_vert(grid, square, unsolved=False):
    """ get column minus reference square """

    related = []

    for row in grid.grid:
        if row[square.col] != square:
            if not unsolved:
                related.append(row[square.col])
            elif not row[square.col].answer:
                related.append(row[square.col])
    return related



def get_area(grid, square, unsolved=False):
    """ get 3x3 area minus reference square """

    related = []

    arow = math.trunc(square.row/3)*3
    acol = math.trunc(square.col/3)*3

    for row in range(arow, arow+3):
        for col in range(acol, acol+3):
            if grid.grid[row][col] != square:

                if not unsolved:
                    related.append(grid.grid[row][col])
                elif not grid.grid[row][col].answer:
                    related.append(grid.grid[row][col])

    return related


def get_related(grid, square, unsolved=False):
    """ visit the row, column and area of a particular square """

    related = []

    related.extend(get_horz(grid, square, unsolved))
    related.extend(get_vert(grid, square, unsolved))
    related.extend(get_only_area(grid, square, unsolved))

    return related



def get_col_pos(grid, position, answered=False):
    """ get column at position, optionally skipping answered squares """

    squares = []
    possibles = []

    for row in grid.grid:
        if not answered and row[position].answer:
            continue
        squares.append(row[position])
        if len(row[position].possibles) > 1:
            possibles.extend(row[position].possibles)

    return squares, list(set(possibles))



def get_row_pos(grid, position, answered=False):
    """ get row at position, optionally skipping answered squares """

    squares = []
    possibles = []

    for col in grid.grid[position]:
        if not answered and col.answer:
            continue
        squares.append(col)
        if len(col.possibles) > 1:
            possibles.extend(col.possibles)

    return squares, list(set(possibles))



def get_col(grid, position, answered=False):
    """ get column at position, optionally skipping answered squares """

    squares = []

    for row in grid.grid:
        if not answered and row[position].answer:
            continue
        squares.append(row[position])

    return squares



def get_row(grid, position, answered=False):
    """ get row at position, optionally skipping answered squares """

    squares = []

    for col in grid.grid[position]:
        if not answered and col.answer:
            continue
        squares.append(col)

    return squares



def get_area_now(grid, arow, acol, answered=False):
    """ get 3x3 area by starting postion """

    squares = []
    possibles = []

    for brow in range(arow, arow+3):
        for bcol in range(acol, acol+3):
            if not answered and grid.grid[brow][bcol].answer:
                continue
            squares.append(grid.grid[brow][bcol])
            if len(grid.grid[brow][bcol].possibles) > 1:
                possibles.extend(grid.grid[brow][bcol].possibles)

    return squares, list(set(possibles))



def get_area_num(grid, num, answered=False):
    """ get 3x3 area by number 0-8 """

    starts = [[0, 0], [0, 3], [0, 6], [3, 0], [3, 3], [3, 6], [6, 0], [6, 3], [6, 6]]

    arow, acol = starts[num]

    return get_area_now(grid, arow, acol, answered)



def get_area_xy(grid, row, col, answered=False):
    """ get 3x3 area by starting postion """

    arow = math.trunc(row/3)*3
    acol = math.trunc(col/3)*3

    return get_area_now(grid, arow, acol, answered)




def sets_of_4(num, possibles, sets):
    """ get all possible sets of four numbers """

    for val1 in possibles:
        for val2 in possibles[1:]:
            for val3 in possibles[2:]:
                for val4 in possibles[3:]:
                    a_set = [val1]
                    if val2 not in a_set and val2 > val1:
                        a_set.append(val2)
                    if val3 not in a_set and val3 > val2:
                        a_set.append(val3)
                    if val4 not in a_set and val4 > val3:
                        a_set.append(val4)
                    if len(a_set) == num:
                        sets.append(a_set)



def sets_of_3(num, possibles, sets):
    """ get all possible sets of three numbers """

    for val1 in possibles:
        for val2 in possibles[1:]:
            for val3 in possibles[2:]:
                a_set = [val1]
                if val2 not in a_set and val2 > val1:
                    a_set.append(val2)
                if val3 not in a_set and val3 > val2:
                    a_set.append(val3)
                if len(a_set) == num:
                    sets.append(a_set)



def get_sets(possibles, num):
    """ get all the possible sets of num """

    sets = []

    if len(possibles) < num:
        return sets

    a_set = []

    if num == 4:
        sets_of_4(num, possibles, sets)

    elif num == 3:
        sets_of_3(num, possibles, sets)

    else:
        for val1 in possibles:
            for val2 in possibles[1:]:
                a_set = [val1]
                if val2 not in a_set and val2 > val1:
                    a_set.append(val2)
                if len(a_set) == num:
                    sets.append(a_set)

    #print('sets='+str(sets))

    return sets



def get_only_area(grid, square, unsolved=False):
    """ get 3x3 area minus reference square, its row or column """

    related = []

    arow = math.trunc(square.row/3)*3
    acol = math.trunc(square.col/3)*3

    for row in range(arow, arow+3):
        for col in range(acol, acol+3):
            if row != square.row and col != square.col:
                if not unsolved:
                    related.append(grid.grid[row][col])
                elif not grid.grid[row][col].answer:
                    related.append(grid.grid[row][col])

    return related



def get_sectioned_horz(grid, square):
    """ get 3x3 area minus reference square, its row or column """

    a_row = []
    o_row = []
    rest = []

    arow = math.trunc(square.row/3)*3
    acol = math.trunc(square.col/3)*3

    for row in range(arow, arow+3):
        for col in range(acol, acol+3):
            if row != square.row:
                rest.append(grid.grid[row][col])
            else:
                a_row.append(grid.grid[row][col])

    for col in range(0, 9):
        if col < acol or col >= acol+3:
            o_row.append(grid.grid[square.row][col])

    return a_row, o_row, rest



def get_sectioned_vert(grid, square):
    """ get 3x3 area minus reference square, its row or column """

    a_col = []
    o_col = []
    rest = []

    arow = math.trunc(square.row/3)*3
    acol = math.trunc(square.col/3)*3

    for row in range(arow, arow+3):
        for col in range(acol, acol+3):
            if col != square.col:
                rest.append(grid.grid[row][col])
            else:
                a_col.append(grid.grid[row][col])

    for row in range(0, 9):
        if row < arow or row >= arow+3:
            o_col.append(grid.grid[row][square.col])

    return a_col, o_col, rest


def position_in(target, squares):
    """ check if squares coordinates in squares """

    for square in squares:
        if target.row == square.row and target.col == square.col:
            return True

    return False



def get_possibles(grid):
    """ get all remaining possibles """

    possibles = []

    for row in grid.grid:
        for square in row:
            if len(square.possibles) > 1:
                possibles.extend(square.possibles)
    return list(set(possibles))



def get_unsolved(grid):
    """ get all remaining unsolved """

    unsolved = []

    for row in grid.grid:
        for square in row:
            if len(square.possibles) > 1:
                unsolved.append(square)
    return unsolved



def print_row(row):
    """ print a row of squares """

    for square in row:
        if square.color:
            print('    '+str(square)+' color='+str(square.color))
        else:
            print('    '+str(square))



def print_rows(rows):
    """ print an array of squares """

    for row in rows:
        print('row:')
        print_row(row)
