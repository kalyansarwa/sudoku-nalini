""" This module has the workhorse functions for games """
import re
import math
import copy

from django.core.exceptions import ObjectDoesNotExist
from games.models import Game, Grid
from games.rules import not_me, only_me, get_related, blockers, twins, hidden_twins, \
    triplets, hidden_triplets, quads, hidden_quads
from games.advanced_rules import xwing, xywing, colors, swordfish


RULES = [not_me, only_me, twins, blockers, hidden_twins, triplets, hidden_triplets,
         quads, hidden_quads, xwing, xywing, colors, swordfish
         ]


def set_square(square, grid, val):
    """ Set the value & possibles """

    if not square.answer:
        grid.solved += 1
    square.answer = val
    square.possibles = [val]



def print_squares(squares):
    """ print an array of squares """

    sq_str = ''
    for square in squares:
        sq_str += str(square) + ', '

    print(sq_str[0:-1])



def json_squares(squares):
    """ return array of squares as json """

    j_squares = []

    for square in squares:
        j_squares.append(square.as_json())
    return j_squares



def update_possibles(grid, solve=False):
    """ Go thru the grid and adjust possibles based answers """

    for row in grid.grid:
        for square in row:
            if square.answer and len(square.possibles) > 1:
                square.possibles = [square.answer]
            if square.answer:
                related = get_related(grid, square)
                vals = [square.answer]
                for rel in related:
                    rel.not_possible(grid, vals, solve)



def check_answers(grid):
    """ Go thru the grid and check answers """

    grid.solved = 0
    checked = 1

    for row in grid.grid:
        for square in row:
            if not square.answer:
                continue
            related = get_related(grid, square)
            for rel in related:
                if rel.answer and square.answer and rel.answer == square.answer:
                    square.wrong = True
                    rel.wrong = True
                    checked = 0

            if not square.wrong:
                grid.solved += 1
                if len(square.possibles) > 1:
                    square.possibles = [square.answer]
                    grid.changed.append(square)

    return grid.solved == 81, checked



def get_game(request, errors):
    """ retrieve the game from POST data, return grid"""

    if request.POST.get("game_id"):
        gid = int(request.POST.get("game_id"))

    else:
        errors.append('Could not get active game')
        return None, None

    try:
        game = Game.objects.get(id=gid)
    except ObjectDoesNotExist:
        errors.append('Game '+str(gid)+' not found')
        return None, None

    grid = Grid()
    grid.load(game)

    return game, grid



def update_game(request, errors):
    """ update the game from POST data, return grid"""

    game, grid = get_game(request, errors)

    if not grid:
        return game, grid

    for key, value in request.POST.items():
        #print('key='+str(key)+' value='+str(value))
        if value:
            update_square(grid, key, value)

    update_possibles(grid, errors)

    return game, grid



def display(grid):
    """ Transform the game for display purposes """

    dgrid = [
        [[[], [], []],
         [[], [], []],
         [[], [], []]],
        [[[], [], []],
         [[], [], []],
         [[], [], []]],
        [[[], [], []],
         [[], [], []],
         [[], [], []]]
    ]

    for i, row in enumerate(grid.grid):
        for j, col in enumerate(row):
            dgrid[math.trunc(i/3)][math.trunc(j/3)][i%3].append(col)

    return dgrid



def update_square(grid, key, value):
    """ update the grid with values entered by player answer-row2col3 """

    if key[0:7] == 'answer-':
        row = int(key[10])
        col = int(key[14])
        grid.grid[row][col].answer = int(value)

    elif key[0:7] == 'pencil-':
        row = int(key[10])
        col = int(key[14])
        grid.grid[row][col].pencil = value



def check_given(given):
    """ check that input conforms to a valid sudoku """

    clean = ''
    digits = re.compile('[0-9]')

    #print('given='+given)

    count = 0

    for i, give in enumerate(given):
        if digits.search(give) is not None:
            clean += given[i]
            count += 1
            if count and count%9 == 0:
                clean += '\n'
            elif count and count%3 == 0:
                clean += ' '

    if count != 81:
        return None

    #print('clean='+clean)

    return clean


def update_transcript(transcript, message):
    """ conditionally update the transcript """

    if transcript is not None and message not in transcript:
        transcript.append(message)



def solve_it(grid, force, transcript=None):
    """ Go thru the grid and adjust possibles based answers """

    rule = 0
    iterations = 0

    while grid.solved < 81:

        s_solved = grid.solved
        chan_len = len(grid.changed)

        #print('Trying rule '+str(RULES[rule].__name__))

        func = RULES[rule]

        iterations += 1

        okay = func(grid)

        #grid.print()
        if not okay:
            update_transcript(transcript, 'Failed while executing rule '+func.__name__)
            return

        done, okay = check_answers(grid)

        if not okay:
            update_transcript(transcript,
                              'Check answers failed while executing rule '+func.__name__)
            return

        if done:
            update_transcript(transcript, 'Solved the puzzle in '+str(iterations)+' rounds')
            return

        if grid.solved == s_solved and chan_len == len(grid.changed):
            rule += 1
            if rule >= len(RULES):
                if force:
                    # If current strategies have failed, try brute force
                    update_transcript(transcript,
                                      'Failed to solve puzzle with rules, trying brute force')
                    brute_force(grid, transcript)
                else:
                    update_transcript(transcript, 'Failed to solve puzzle')

                return
        else:
            update_transcript(transcript, 'Used rule '+func.__name__)
            rule = 0
            #print('restarting rules')

    print('grid.solved='+str(grid.solved))
    grid.print()

    return



def brute_force(grid, transcript):
    """ recursively try all possible solutions until one works """

    #grid.print()
    entry = None

    # find the next square where there are possibles
    for row in grid.grid:
        for square in row:
            if not square.answer:
                entry = square
                break
        if entry:
            break

    if entry:
        possibles = entry.possibles
        #print('possibles='+str(possibles))
        for possible in possibles:
            #print('possible='+str(possible))

            grid_copy = copy.deepcopy(grid)
            set_square(grid_copy.grid[entry.row][entry.col], grid_copy, possible)
            ccopy = copy.deepcopy(grid_copy.grid[entry.row][entry.col])
            grid_copy.changed.append(ccopy)

            #print('Trying brute force on '+str(grid_copy.grid[entry.row][entry.col]))
            #grid_copy.print()

            solve_it(grid_copy, True, transcript)

            if grid_copy.solved == 81 and not grid_copy.errors:
                #print('Solved puzzle with brute force')
                grid.grid = grid_copy.grid
                grid.solved = grid_copy.solved
                grid.changed = grid_copy.changed
                grid.errors = grid_copy.errors
                return
    else:
        update_transcript(transcript, 'Failed to solve puzzle even with brute force')

    return
