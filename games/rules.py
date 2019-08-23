""" This module has the all the basic rules functions for games """
import copy

from games.sections import get_horz, get_vert, get_area, get_row_pos, get_col_pos, get_area_num, \
    get_related, get_sectioned_horz, get_sectioned_vert, get_sets



def not_me(grid):
    """ Remove square's value from related square's possibles """

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
            ucopy = copy.deepcopy(square)
            square.answer = val
            grid.solved += 1
            square.possibles = [val]
            rcopy = copy.deepcopy(square)
            grid.changed.append(rcopy)
            return True
    return False



def only_me(grid):
    """ Go thru grid looking for square possibles unique to the row, col or area"""

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

            okay = blocker_check(grid, square, o_line, rest)

            if not okay:
                return False

            a_line, o_line, rest = get_sectioned_vert(grid, square)

            okay = blocker_check(grid, square, o_line, rest)

            if not okay:
                return False

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
        ucopy = copy.deepcopy(square)
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
            okay = purge_square(grid, square, mvals)
            if not okay:
                return False

    return True



def open_matches(grid, num):
    """ Look for matches (twins, triplets, etc.) and purge the matched mvals from others """

    for i in range(0, 9):
        unsolved, possibles = get_row_pos(grid, i)

        if len(unsolved) < num:
            continue

        sets = get_sets(possibles, num)
        for mvals in sets:
            okay = match_check(grid, unsolved, num, mvals)
            if not okay:
                return False

    for i in range(0, 9):
        unsolved, possibles = get_col_pos(grid, i)

        if len(unsolved) < num:
            continue

        sets = get_sets(possibles, num)
        for mvals in sets:
            okay = match_check(grid, unsolved, num, mvals)
            if not okay:
                return False

    for i in range(0, 9):
        unsolved, possibles = get_area_num(grid, i)

        if len(unsolved) < num:
            continue

        sets = get_sets(possibles, num)
        for mvals in sets:
            okay = match_check(grid, unsolved, num, mvals)
            if not okay:
                return False

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
        okay = purge_square_not(grid, match, mvals)
        if not okay:
            print('Problem purging square '+str(match)+' of values other than '+str(mvals))
            return False

    return True



def hidden_matches(grid, num):
    """ find matches that might be hidden in other possibles """

    for i in range(0, 9):
        unsolved, possibles = get_row_pos(grid, i)
        sets = get_sets(possibles, num)
        for mvals in sets:
            okay = hidden_match_check(grid, unsolved, num, mvals)
            if not okay:
                return False

    for i in range(0, 9):
        unsolved, possibles = get_col_pos(grid, i)
        sets = get_sets(possibles, num)
        for mvals in sets:
            okay = hidden_match_check(grid, unsolved, num, mvals)
            if not okay:
                return False

    for i in range(0, 9):
        unsolved, possibles = get_area_num(grid, i)
        sets = get_sets(possibles, num)
        for mvals in sets:
            okay = hidden_match_check(grid, unsolved, num, mvals)
            if not okay:
                return False

    return True



def twins(grid):
    """ wrapper to matches with 2 """

    okay = open_matches(grid, 2)

    return okay



def hidden_twins(grid):
    """ wrapper to hidden_matches with 3 """

    okay = hidden_matches(grid, 2)

    return okay


def triplets(grid):
    """ wrapper to matches with 3 """

    okay = open_matches(grid, 3)

    return okay



def hidden_triplets(grid):
    """ wrapper to hidden_matches with 3 """

    okay = hidden_matches(grid, 3)

    return okay



def quads(grid):
    """ wrapper to matches with 4 """

    okay = open_matches(grid, 4)

    return okay



def hidden_quads(grid):
    """ wrapper to hidden_matches with 4 """

    okay = hidden_matches(grid, 4)

    return okay
