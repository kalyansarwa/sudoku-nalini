""" This module has more advanced rules functions for games """
import copy

from games.sections import get_horz, get_vert, get_area, get_row, get_col, get_row_pos, \
    get_col_pos, position_in, get_unsolved, get_possibles, get_only_area#, print_rows


def xwing(grid):
    """ find candidates in a box shape """

    for i in range(0, 9):
        unsolved, possibles = get_row_pos(grid, i)
        for possible in possibles:
            firsts = xwing_check(unsolved, possible)

            if firsts:
                okay = xwing_row_check(grid, firsts, possible)

    for i in range(0, 9):
        unsolved, possibles = get_col_pos(grid, i)
        for possible in possibles:
            firsts = xwing_check(unsolved, possible)

            if firsts:
                okay = xwing_col_check(grid, firsts, possible)
                if not okay:
                    return False

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

            okay = square.not_possible(grid, [possible], True)
            if not okay:
                return False

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

    okay = remove_excepts(grid, squares, possible, [firsts[0], seconds[0]])
    if not okay:
        return False

    squares = get_col(grid, firsts[1].col)

    okay = remove_excepts(grid, squares, possible, [firsts[1], seconds[1]])
    if not okay:
        return False

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

    #print('got col xwing with '+str(possible)+' starting with :')
    #print(str(firsts[0]))
    #print(str(firsts[1]))
    #print(str(seconds[0]))
    #print(str(seconds[1]))

    squares = get_row(grid, firsts[0].row)

    okay = remove_excepts(grid, squares, possible, [firsts[0], seconds[0]])
    if not okay:
        return False

    squares = get_row(grid, firsts[1].row)
    okay = remove_excepts(grid, squares, possible, [firsts[1], seconds[1]])
    if not okay:
        return False

    return True



def xywing(grid):
    """ find candidate pairs in a Y shape """

    for i in range(0, 8):
        unsolved, possibles = get_row_pos(grid, i)
        if len(possibles) < 3:
            continue
        for j, square in enumerate(unsolved):
            if len(square.possibles) == 2:
                okay = xywing_check(grid, square, unsolved[j+1:])
                if not okay:
                    return False

    for i in range(0, 8):
        unsolved, possibles = get_col_pos(grid, i)
        if len(possibles) < 3:
            continue
        for j, square in enumerate(unsolved):
            if len(square.possibles) == 2:
                okay = xywing_check(grid, square, unsolved[j+1:])
                if not okay:
                    return False

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
                    okay = xywing_y_col(grid, firsts, pair)
                elif firsts[0].col == firsts[1].col:
                    okay = xywing_y_row(grid, firsts, pair)
                if not okay:
                    return False

    return True



def xywing_y_col(grid, firsts, pair):
    """ look for a square with the pair as possibles along the cols """

    related = get_vert(grid, firsts[0])

    for square in related:

        if pair.issubset(square.possibles) and pair.issuperset(square.possibles):

            #print('found bottom: '+str(square))

            target = grid.grid[square.row][firsts[1].col]

            #print('found target: '+str(target))

            okay = xywing_target(grid, target, square, firsts[1])
            if not okay:
                return False

    related = get_vert(grid, firsts[1])

    for square in related:

        if pair.issubset(square.possibles) and pair.issuperset(square.possibles):

            target = grid.grid[square.row][firsts[0].col]

            #print('found target: '+str(target))

            okay = xywing_target(grid, target, square, firsts[0])
            if not okay:
                return False

    return True



def xywing_y_row(grid, firsts, pair):
    """ look for a square with the pair as possibles along the rows """

    related = get_horz(grid, firsts[0])

    for square in related:

        if pair.issubset(square.possibles) and pair.issuperset(square.possibles):

            target = grid.grid[square.col][firsts[1].row]

            okay = xywing_target(grid, target, square, firsts[1])
            if not okay:
                return False

    related = get_horz(grid, firsts[1])

    for square in related:

        if pair.issubset(square.possibles) and pair.issuperset(square.possibles):

            target = grid.grid[square.col][firsts[0].row]

            okay = xywing_target(grid, target, square, firsts[0])
            if not okay:
                return False

    return True



def xywing_target(grid, target, square, other):
    """ Remove the shared possible from the target """

    shared = set(square.possibles).intersection(other.possibles)

    if shared:
        #print('Removing '+str(shared)+' from '+str(target))
        okay = target.not_possible(grid, list(shared), True)
        if not okay:
            return False

    return True



def colors(grid):
    """ find candidates in where there are only 2 in a related area,
        then try to follow chain, alternating "colors"  """

    solved = grid.solved
    changed = len(grid.changed)

    # go thru all the squares, all their possibles, and look for chains of only 2 in related squares

    remaining = get_unsolved(grid)
    for square in remaining:
        unsolved = get_horz(grid, square, True)
        for possible in square.possibles:
            #print('Doing possible '+str(possible)+' for square '+str(square))
            chain = find_pair(square, unsolved, possible)
            if chain:
                okay = find_next(grid, chain, possible, 'row')
                if not okay:
                    return okay
                if grid.solved > solved or len(grid.changed) > changed:
                    return True

            #TO DO: find some way to get only unsolved
            unsolved = get_vert(grid, square, True)
            chain = find_pair(square, unsolved, possible)
            if chain:
                okay = find_next(grid, chain, possible, 'col')
                if not okay:
                    return okay
                if grid.solved > solved or len(grid.changed) > changed:
                    return True


            unsolved = get_area(grid, square, True)
            chain = find_pair(square, unsolved, possible)
            if chain:
                okay = find_next(grid, chain, possible, 'area')
                if not okay or grid.solved > solved or len(grid.changed) > changed:
                    return okay

    return True



def find_pair(square, unsolved, possible):
    """ find squares that contain possible and stash them if there are only two """

    squares = [square]

    for uns in unsolved:
        if possible in uns.possibles:
            squares.append(uns)

    if len(squares) == 2:
        squares[0].color = True
        squares[1].color = False
        return squares

    return None


def sc_check_related(grid, related, candidate, chain, squares):
    """ go thru the related squares checking for chaining """

    for rel in related:
        # changed this logic, its only 2 of the candidate in related
        if candidate in rel.possibles:
            got_it = check_chain(grid, chain, rel)
            if got_it:
                okay = rel.not_possible(grid, [candidate], True)
                return got_it, okay
            squares.append(rel)
    return False, False



def find_next(grid, chain, candidate, last_find):
    """ look for next candidate square in chain """

    end = chain[-1]

    if last_find != 'row':
        related = get_horz(grid, end, True)
        squares = []

        got_it, okay = sc_check_related(grid, related, candidate, chain, squares)

        if got_it:
            return okay

        if len(squares) == 1 and not position_in(squares[0], chain):
            squares[0].color = not end.color

            cchain = copy.deepcopy(chain)
            cchain.extend(squares)
            okay = find_next(grid, cchain, candidate, 'row')
            if not okay or not cchain:
                chain.clear()
                return okay

    if last_find != 'col':
        related = get_vert(grid, end, True)
        squares = []

        got_it, okay = sc_check_related(grid, related, candidate, chain, squares)

        if got_it:
            return okay

        if len(squares) == 1 and not position_in(squares[0], chain):
            squares[0].color = not end.color

            cchain = copy.deepcopy(chain)
            cchain.extend(squares)
            okay = find_next(grid, cchain, candidate, 'row')
            if not okay or not cchain:
                chain.clear()
                return okay

    if last_find != 'area':

        related = get_area(grid, end, True)
        squares = []

        got_it, okay = sc_check_related(grid, related, candidate, chain, squares)

        if got_it:
            return okay

        if len(squares) == 1 and not position_in(squares[0], chain):
            squares[0].color = not end.color

            cchain = copy.deepcopy(chain)
            cchain.extend(squares)
            okay = find_next(grid, cchain, candidate, 'area')
            if not okay or not cchain:
                chain.clear()
                return okay

    return True



def check_chain(grid, chain, square):
    """ See if the new square end point can see both colors """

    if position_in(square, chain):
        return False

    can_see = []


    for chn in chain:
        if (chn.row == square.row or chn.col == square.col):
            can_see.append(chn.color)

        related = get_only_area(grid, square, True)
        if position_in(square, related):
            can_see.append(chn.color)

    if len(list(set(can_see))) > 1:
        # if can see more than 1 color
        #print('Colors chain=')
        #print_row(chain)
        #print('Colors target='+str(square)+' color='+str(square.color))

        chain.clear()
        return True

    return False


def swordfish(grid):
    """ find 2-3 occurances of candidate in 3 cols or 3 rows. Then remove extras
        from cols if found in 3 rows, or rows if found in cols """

    solved = grid.solved
    changed = len(grid.changed)

    all_possibles = get_possibles(grid)

    for possible in all_possibles:
        #print('swordfish trying with '+str(possible))
        okay = sfish_possible(grid, possible)

        if not okay:
            return False
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

    #print('SF possible: '+str(possible))
    #print('sf_rows='+str(sf_rows))
    #print('sf_cols='+str(sf_cols))

    # test for rows-wise swordfish
    sf_set, slots = sf_check(sf_rows)
    if sf_set:
       # remove extra possibles
        for sfs in sf_set:
            squares = get_col(grid, sfs)
            for square in squares:
                if square.row not in slots:
                    okay = square.not_possible(grid, [possible], True)
                    if not okay:
                        return False

    # test for cols-wise swordfish
    sf_set, slots = sf_check(sf_cols)
    if sf_set:
        #remove extra possibles
        for sfs in sf_set:
            squares = get_row(grid, sfs)
            for square in squares:
                if square.col not in slots:
                    okay = square.not_possible(grid, [possible], True)
                    if not okay:
                        return False

    return True



def sf_check(sf_rc):
    """ check for the pattern in rows or cols """

    for i in range(0, 9):
        if len(sf_rc[i]) > 1 and len(sf_rc[i]) < 4:
            test_set = sf_rc[i]
            #print('initial test_set='+str(test_set))
            slots = [i]
            for j in range(0, 9):
                if i != j and len(sf_rc[j]) > 1 and len(sf_rc[j]) < 4 and \
                    len(list(set(test_set+sf_rc[j]))) < 4:
                    slots.append(j)
                    test_set = list(set(test_set+sf_rc[j]))
                    #print('current test_set='+str(test_set))
                    if len(slots) == 3 and len(test_set) == 3:
                        #print('SF sf_set ='+str(test_set))
                        #print('SF slots = '+str(slots))
                        return test_set, slots
    return None, None
