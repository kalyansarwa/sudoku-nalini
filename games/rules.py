""" This module has the all the basic rules functions for games """
import copy

from games.sections import get_horz, get_vert, get_area, get_row_pos, get_col_pos, get_area_num, \
    get_related, get_sectioned_horz, get_sectioned_vert, get_sets



def not_me(grid):
    """
    If a square has been set to a particular number, then all related squares cannot be that number
    Remove square's value from related square's possibles """

    for row in grid.grid:
        for square in row:

            if not square.answer:
                continue

            related = get_related(grid, square)

            vals = [square.answer]
            for rel in related:
                if rel.answer:
                    continue
                rel.not_possible(grid, vals, True)
                if rel.wrong:
                    return False

    return True



def unique_check(grid, square, vals, related):
    """ workhorse function for only me """

    for val in vals:
        unique = True
        for rel in related:
            if val in rel.possibles:
                unique = False
        if unique:
            square.answer = val
            grid.solved += 1
            square.possibles = [val]
            rcopy = copy.deepcopy(square)
            grid.changed.append(rcopy)
            return True
    return False



def only_me(grid):
    """
    If a possible value for the square isn't present in any related squares, then
    that square must be that value.
    Go thru grid looking for square possibles unique to the row, col or area"""

    for row in grid.grid:
        for square in row:

            if square.answer:
                continue

            vals = square.possibles

            if len(vals) == 1:
                square.set_answer(grid, vals[0], True)
                continue

            related = get_horz(grid, square)
            got_it = unique_check(grid, square, vals, related)
            if got_it:
                break

            related = get_vert(grid, square)
            got_it = unique_check(grid, square, vals, related)
            if got_it:
                break

            related = get_area(grid, square)
            got_it = unique_check(grid, square, vals, related)

    return True



def blocker_check(grid, square, o_line, rest):
    """ workhorse funtion for blockers """

    for val in square.possibles:
        blocked = True

        for square2 in o_line:
            if val in square2.possibles:
                blocked = False

        if blocked:
            for square2 in rest:
                square2.not_possible(grid, [val], True)
                if square2.wrong:
                    print('Problem in blocker_check with square '+str(square2)+' removing value '+\
                           str(val)+' blocked by square '+str(square))
                    return False

        blocked = True
        for square2 in rest:
            if val in square2.possibles:
                blocked = False
        if blocked:
            for square2 in o_line:
                square2.not_possible(grid, [val], True)
                if square2.wrong:
                    print('Problem in blocker_check with square '+str(square2)+' removing value '+\
                           str(val)+' blocked by square '+str(square))
                    return False
    return True



def blockers(grid):
    """ find combos of values that eliminate other square's possibles """

    for row in grid.grid:
        for square in row:

            a_line, o_line, rest = get_sectioned_horz(grid, square)

            blocker_check(grid, square, o_line, rest)

            a_line, o_line, rest = get_sectioned_vert(grid, square)

            blocker_check(grid, square, o_line, rest)


    return True



def purge_square(grid, square, mvals):
    """ remove the matched values from the square """

    vals = []
    for val in square.possibles:
        if val in mvals:
            vals.append(val)
    if vals:
        square.not_possible(grid, vals, True)

        if square.wrong:
            return False

    return True



def purge_square_not(grid, square, mvals):
    """ remove values other than the matched values from the square """

    vals = []
    for val in square.possibles:
        if val not in mvals:
            vals.append(val)
    if vals:
        square.not_possible(grid, vals, True)
        ccopy = copy.deepcopy(square)
        grid.changed.append(ccopy)

        if square.wrong:
            return False

    return True



def match_check(grid, unsolved, num, mvals):
    """ workhorse function for matches """

    matches = []

    # look for num squares that match the mvals
    for square in unsolved:
        if square.possibles == mvals:
            matches.append(square)

    if len(matches) != num:
        return True

    #print('got '+str(num)+ 'matches:')
    #for match in matches:
        #print(str(match)+' possibles: '+str(match.possibles))

    for square in unsolved:
        if square not in matches:
            purge_square(grid, square, mvals)

    return True



def open_matches(grid, num):
    """ Look for matches (twins, triplets, etc.) in a row, column or area, then purge the matched
        values from the possibles of the other squares in that row, column or area """

    for i in range(0, 9):
        unsolved, possibles = get_row_pos(grid, i)

        if len(unsolved) < num:
            continue

        sets = get_sets(possibles, num)
        for mvals in sets:
            match_check(grid, unsolved, num, mvals)

    for i in range(0, 9):
        unsolved, possibles = get_col_pos(grid, i)

        if len(unsolved) < num:
            continue

        sets = get_sets(possibles, num)
        for mvals in sets:
            match_check(grid, unsolved, num, mvals)

    for i in range(0, 9):
        unsolved, possibles = get_area_num(grid, i)

        if len(unsolved) < num:
            continue

        sets = get_sets(possibles, num)
        for mvals in sets:
            match_check(grid, unsolved, num, mvals)

    return True



def hidden_match_check(grid, unsolved, num, mvals):
    """ workhorse function for matchs """

    if len(unsolved) <= num:
        return True

    matches = []

    for square in unsolved:

        matched = False
        for item in mvals:
            if item in square.possibles:
                matched = True
        if matched:
            matches.append(square)

    if len(matches) != num:
        return True

    # check that we got at least one of each mvals
    for item in mvals:
        missing = True
        for match in matches:
            if item in match.possibles:
                missing = False
        if missing:
            return True

    for match in matches:
        purge_square_not(grid, match, mvals)

    return True



def hidden_matches(grid, num):
    """ find matches that might be mixed in with other possibles. If you find twins, triplets, etc.
    then remove the other possibles from the squares containing the match. """

    for i in range(0, 9):
        unsolved, possibles = get_row_pos(grid, i)
        sets = get_sets(possibles, num)
        for mvals in sets:
            hidden_match_check(grid, unsolved, num, mvals)

    for i in range(0, 9):
        unsolved, possibles = get_col_pos(grid, i)
        sets = get_sets(possibles, num)
        for mvals in sets:
            hidden_match_check(grid, unsolved, num, mvals)

    for i in range(0, 9):
        unsolved, possibles = get_area_num(grid, i)
        sets = get_sets(possibles, num)
        for mvals in sets:
            hidden_match_check(grid, unsolved, num, mvals)

    return True



def twins(grid):
    """ wrapper to matches with 2 """

    open_matches(grid, 2)

    return True



def hidden_twins(grid):
    """ wrapper to hidden_matches with 3 """

    hidden_matches(grid, 2)

    return True


def triplets(grid):
    """ wrapper to matches with 3 """

    open_matches(grid, 3)

    return True



def hidden_triplets(grid):
    """ wrapper to hidden_matches with 3 """

    hidden_matches(grid, 3)

    return True



def quads(grid):
    """ wrapper to matches with 4 """

    open_matches(grid, 4)

    return True



def hidden_quads(grid):
    """ wrapper to hidden_matches with 4 """

    hidden_matches(grid, 4)

    return True
