""" This module has more advanced rules functions for games """
from collections import defaultdict
import copy

from games.sections import get_horz, get_vert, get_row, get_col, get_row_pos, \
    get_col_pos, get_unsolved, get_possibles#, print_row



COLORS = [
    ['blue', 'orange'],
    ['purple', 'yellow'],
    ['green', 'red'],
    ['lightcyan', 'coral'],
    ['palevioletred', 'lemonchiffon'],
    ['greenyellow', 'rosybrown'],
    ['lightblue', 'peachpuff'],
    ['plum', 'lightyellow'],
    ['lightgreen', 'lightpink'],
]


def xwing(grid):
    """ XWing is a technique for removing possibles, not finding a direct solution.
        If you can find exactly two matching candidates in a row, and then
        find exactly two in another row (in a box shape), then any other of the same candidate
        above or below in the same to columns can be eliminated from possible.

        If you find a box in columns, the same is true for rows.
        """

    for i in range(0, 9):
        unsolved, possibles = get_row_pos(grid, i)
        for possible in possibles:
            firsts = xwing_check(unsolved, possible)

            if firsts:
                xwing_row_check(grid, firsts, possible)

    for i in range(0, 9):
        unsolved, possibles = get_col_pos(grid, i)
        for possible in possibles:
            firsts = xwing_check(unsolved, possible)

            if firsts:
                xwing_col_check(grid, firsts, possible)

    return True



def xwing_check(unsolved, possible):
    """ look for cases where there are exactly 2 occurance of possible in unsolved """

    firsts = []
    for square in unsolved:
        if possible in square.possibles:
            firsts.append(square)

    if len(firsts) == 2:
        return firsts

    return None


def remove_excepts(grid, squares, possible, excepts):
    """ remove the possible from the list of squares unless its in excepts """

    for square in squares:
        if square not in excepts and  possible in square.possibles:

            square.not_possible(grid, [possible], True)

    return True



def xwing_row_check(grid, firsts, possible):
    """ see if you can locate the same possible pair in the same columns in a following row,
        if so remove all possibles from rest of column """

    seconds = []

    start = firsts[0].row
    for i in range(start+1, 9):
        squares, possibles = get_row_pos(grid, i)
        if possible not in possibles:
            continue

        for square in squares:
            if square.col != firsts[0].col and square.col != firsts[1].col and \
                possible in square.possibles:
                seconds = []
                break
            if (square.col == firsts[0].col or square.col == firsts[1].col) and \
                possible in square.possibles:
                seconds.append(square)

        if len(seconds) == 2:
            # just found the second row!
            break

    if len(seconds) != 2:
        return True

    squares = get_col(grid, firsts[0].col)

    remove_excepts(grid, squares, possible, [firsts[0], seconds[0]])

    squares = get_col(grid, firsts[1].col)

    remove_excepts(grid, squares, possible, [firsts[1], seconds[1]])

    return True



def xwing_col_check(grid, firsts, possible):
    """ see if you can locate the same possible pair in the same rows in a following column,
        if so remove all possibles from rest of row """

    seconds = []

    start = firsts[0].col

    for i in range(start+1, 9):
        squares, possibles = get_col_pos(grid, i)
        if possible not in possibles:
            continue

        for square in squares:
            if square.row != firsts[0].row and square.row != firsts[1].row and \
                possible in square.possibles:
                seconds = []
                break
            if (square.row == firsts[0].row or square.row == firsts[1].row) and \
                possible in square.possibles:
                seconds.append(square)

        if len(seconds) == 2:
            # just found the second row!
            break

    if len(seconds) != 2:
        return True

    squares = get_row(grid, firsts[0].row)

    remove_excepts(grid, squares, possible, [firsts[0], seconds[0]])

    squares = get_row(grid, firsts[1].row)
    remove_excepts(grid, squares, possible, [firsts[1], seconds[1]])

    return True



def xywing(grid):
    """ find candidate pairs in a Y shape """

    for i in range(0, 8):
        unsolved, possibles = get_row_pos(grid, i)
        if len(possibles) < 3:
            continue
        for j, square in enumerate(unsolved):
            if len(square.possibles) == 2:
                xywing_check(grid, square, unsolved[j+1:])

    for i in range(0, 8):
        unsolved, possibles = get_col_pos(grid, i)
        if len(possibles) < 3:
            continue
        for j, square in enumerate(unsolved):
            if len(square.possibles) == 2:
                xywing_check(grid, square, unsolved[j+1:])

    return True



def xywing_check(grid, square, unsolved):
    """ look for complementary pair in remaining unsolved """

    pair = []

    for uns in unsolved:
        if len(uns.possibles) != 2:
            continue

        for possible in uns.possibles:
            if possible in square.possibles:
                firsts = [square, uns]
                pair = set(square.possibles).symmetric_difference(uns.possibles)
                if not pair:
                    continue
                if firsts[0].row == firsts[1].row:
                    xywing_y_col(grid, firsts, pair)
                elif firsts[0].col == firsts[1].col:
                    xywing_y_row(grid, firsts, pair)

    return True



def xywing_y_col(grid, firsts, pair):
    """ look for a square with the pair as possibles along the cols """

    related = get_vert(grid, firsts[0])

    for square in related:

        if pair.issubset(square.possibles) and pair.issuperset(square.possibles):

            target = grid.grid[square.row][firsts[1].col]

            xywing_target(grid, target, square, firsts[1])

    related = get_vert(grid, firsts[1])

    for square in related:

        if pair.issubset(square.possibles) and pair.issuperset(square.possibles):

            target = grid.grid[square.row][firsts[0].col]

            xywing_target(grid, target, square, firsts[0])

    return True



def xywing_y_row(grid, firsts, pair):
    """ look for a square with the pair as possibles along the rows """

    related = get_horz(grid, firsts[0])

    for square in related:

        if pair.issubset(square.possibles) and pair.issuperset(square.possibles):

            target = grid.grid[square.col][firsts[1].row]

            xywing_target(grid, target, square, firsts[1])

    related = get_horz(grid, firsts[1])

    for square in related:

        if pair.issubset(square.possibles) and pair.issuperset(square.possibles):

            target = grid.grid[square.col][firsts[0].row]

            xywing_target(grid, target, square, firsts[0])



def xywing_target(grid, target, square, other):
    """ Remove the shared possible from the target """

    shared = set(square.possibles).intersection(other.possibles)

    if shared:
        target.not_possible(grid, list(shared), True)



def swordfish(grid):
    """ This is a strategy to remove possibles. Find 2-3 occurances of candidate in 3 cols or 3
        rows. Then remove extras from cols if found in 3 rows, or rows if found in cols """

    solved = grid.solved
    changed = len(grid.changed)

    all_possibles = get_possibles(grid)

    for possible in all_possibles:
        sfish_possible(grid, possible)

        if grid.solved > solved:
            #print('Swordfish solved '+str(grid.solved-solved)+' squares')
            return True
        if len(grid.changed) > changed:
            #print('Swordfish updated possibles for '+str(len(grid.changed)-changed)+' squares')
            return True

    return True



def sfish_possible(grid, possible):
    """ find all the occurrances of possible """

    sf_rows = [[], [], [], [], [], [], [], [], []]
    sf_cols = [[], [], [], [], [], [], [], [], []]


    unsolved = get_unsolved(grid)
    for square in unsolved:
        if possible in square.possibles:
            sf_rows[square.row].append(square.col)
            sf_cols[square.col].append(square.row)

    # test for rows-wise swordfish
    sf_set, slots = sf_check(sf_rows)
    if sf_set:
       # remove extra possibles
        for sfs in sf_set:
            squares = get_col(grid, sfs)
            for square in squares:
                if square.row not in slots:
                    square.not_possible(grid, [possible], True)

    # test for cols-wise swordfish
    sf_set, slots = sf_check(sf_cols)
    if sf_set:
        #remove extra possibles
        for sfs in sf_set:
            squares = get_row(grid, sfs)
            for square in squares:
                if square.col not in slots:
                    square.not_possible(grid, [possible], True)

    return True



def sf_check(sf_rc):
    """ check for the pattern in rows or cols """

    for i in range(0, 9):
        if len(sf_rc[i]) > 1 and len(sf_rc[i]) < 4:
            test_set = sf_rc[i]
            slots = [i]
            for j in range(0, 9):
                if i != j and len(sf_rc[j]) > 1 and len(sf_rc[j]) < 4 and \
                    len(list(set(test_set+sf_rc[j]))) < 4:
                    slots.append(j)
                    test_set = list(set(test_set+sf_rc[j]))
                    if len(slots) == 3 and len(test_set) == 3:
                        return test_set, slots
    return None, None


def colorize(grid, chain, index):
    """ turn True/False into colors """

    for link in chain:
        if link.color:
            grid.grid[link.row][link.col].color = COLORS[index][0]
        elif link.color is not None:
            grid.grid[link.row][link.col].color = COLORS[index][1]



def simple_colors(grid):
    """ AKA Simple Chaining. This is a strategy to remove possibles. Find possibles in where there
        are only 2 in a related area, then try to follow chain to the next 2 only, alternating
        "colors". Do the whole chain, then if any color appears twice in a related area, then the
        possible in all chained squares of that color are invalid and can be removed. """

    remaining = get_unsolved(grid)
    for square in remaining:

        for possible in square.possibles:
            chain = [{'square': square, 'color':True, 'type': None}]
            chains = [chain]

            while chains:
                # chains exists because its possible to have alternate chains staring from the same
                # square. This is not yet implemented

                chain = chains.pop(0)

                find_next(remaining, chain, chains, possible)

                if len(chain) > 3:
                    if check_chain(grid, remaining, chain, possible):
                        return True

    return True




def find_next(remaining, chain, chains, possible):
    """ look for next candidate square to put in chain """

    end = chain[-1]

    if end['type'] != 'row':
        squares = []
        for square in remaining:
            if square != end['square'] and square.row == end['square'].row and \
                possible in square.possibles:
                squares.append(square)
        if len(squares) == 1 and not in_chain(squares[0], chain):
            chain.append({'square': squares[0], 'color':not end['color'], 'type': 'row'})
            find_next(remaining, chain, chains, possible)
            return

    if end['type'] != 'col':
        squares = []
        for square in remaining:
            if square != end['square'] and square.col == end['square'].col and \
                possible in square.possibles:
                squares.append(square)
        if len(squares) == 1 and not in_chain(squares[0], chain):
            chain.append({'square': squares[0], 'color':not end['color'], 'type': 'col'})
            find_next(remaining, chain, chains, possible)
            return

    if end['type'] != 'area':
        squares = []
        for square in remaining:
            if square != end['square'] and square.area == end['square'].area and \
                possible in square.possibles:
                squares.append(square)
        if len(squares) == 1 and not in_chain(squares[0], chain):
            chain.append({'square': squares[0], 'color':not end['color'], 'type': 'area'})
            find_next(remaining, chain, chains, possible)
            return

    return



def in_chain(square, chain):
    """ check if the square is already in the chain """

    for link in chain:
        if link['square'] == square:
            return True
    return False


def print_chain(chain):
    """ for debugging """

    print(', '.join('square='+str(link['square'])+' color='+str(link['color']) for link in chain))



def color_dicts(chain):
    """ create summary of where colors are in chain """

    color1 = defaultdict(int)
    color2 = defaultdict(int)

    for chn in chain:
        if chn['color']:
            key = 'r'+str(chn['square'].row)
            color1[key] += 1
            key = 'c'+str(chn['square'].col)
            color1[key] += 1
            key = 'a'+str(chn['square'].area)
            color1[key] += 1
        else:
            key = 'r'+str(chn['square'].row)
            color2[key] += 1
            key = 'c'+str(chn['square'].col)
            color2[key] += 1
            key = 'a'+str(chn['square'].area)
            color2[key] += 1

    return color1, color2



def check_chain(grid, remaining, chain, possible):
    """ Definition 1: See if both colors are present in the same unit. If so, that color is
        invalid, remove possibles from all of that color in the chain.
        Definition 2: Can any of the remaining squares with possible see both colors. If so,
        remove THAT square's possible """

    #print('checking chain with possible '+str(possible))
    #print_chain(chain)

    color1, color2 = color_dicts(chain)

    # Definition 1: See if both colors are present in the same unit

    for key, val in color1.items():
        if val > 1:
            # purge all of the possibles for this color out of the chain
            for chn in chain:
                if chn['color']:
                    chn['square'].color = 'red'
                    chn['square'].not_possible(grid, [possible], True)
                else:
                    chn['square'].color = 'green'
                    rcopy = copy.deepcopy(chn['square'])
                    grid.changed.append(rcopy)

            return True

    for key, val in color2.items():
        if val > 1:
            # purge all of the possibles for this color out of the chain
            for chn in chain:
                if not chn['color']:
                    chn['square'].color = 'red'
                    chn['square'].not_possible(grid, [possible], True)
                else:
                    chn['square'].color = 'green'
                    rcopy = copy.deepcopy(chn['square'])
                    grid.changed.append(rcopy)

            return True


    # Definition 2: Can any of the remaining squares with possible see both colors

    for rem in remaining:
        if possible not in rem.possibles or in_chain(rem, chain):
            continue
        clr1 = 0
        clr2 = 0
        # get all colors rem can see
        for key, val in color1.items():
            if key == 'r'+str(rem.row):
                clr1 += 1
            elif key == 'c'+str(rem.col):
                clr1 += 1
            elif key == 'a'+str(rem.area):
                clr1 += 1

        for key, val in color2.items():
            if key == 'r'+str(rem.row):
                clr2 += 1
            elif key == 'c'+str(rem.col):
                clr2 += 1
            elif key == 'a'+str(rem.area):
                clr2 += 1

        if clr1 and clr2:
            rem.not_possible(grid, [possible], True)
            return True

    return False



def multiple_colors(grid):
    """ find multiple chains for candidates, then see if one chain relates to the other so
        as to eliminate the candidate in other (non-chain) cells. Game 71 has this for 6s
        NOT FINISHED """


    # go thru all the squares, all their possibles, and look for chains of only 2 in related squares
    # unlike colors, stash the chains


    return True
