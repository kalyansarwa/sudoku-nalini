""" This module has the views for games """
import random
import copy
import json

from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from .models import Game
from .permissions import get_view_filters
from .games import Grid, display, check_given, update_possibles, check_answers, \
    solve_it, update_game, json_squares
from .forms import GameForm, GamesForm

# Create your views here.


def get_game(gid, errors):
    """ get the game & display stuff from gid """

    try:
        game = Game.objects.get(id=gid)
    except ObjectDoesNotExist:
        errors.append('Game '+str(gid)+' not found')
        return None, None, None

    grid = Grid()
    grid.load(game)

    update_possibles(grid, errors)

    dgrid = display(grid)

    return game, grid, dgrid



def index(request, gid=None):
    """ The base view of the game """

    errors = []
    context = {}
    game = None
    dgrid = None
    done = False
    checked = False

    if request.method == 'POST':

        form = GameForm(request.POST)

        if not form.is_valid():

            errors.append('Form is not valid')
            context = {'errors':errors, 'form': form}
            return redirect('/?errors='+str(errors), context)

        if request.POST.get("get_game"):

            some = Game.objects.filter(level=form.cleaned_data['level'])

            if some:
                game = some[random.randint(0, len(some)-1)]
                return redirect('/'+str(game.id))

            return redirect('/?error=No games at that level')
            #return render(request, 'index.html', context)

        if request.POST.get("check"):

            game, grid = update_game(request, errors)

            if grid:

                done, checked = check_answers(grid)
                update_possibles(grid, errors)

                dgrid = display(grid)

            context = {'game': game, 'errors':errors, 'display':dgrid, 'done': done,
                       'checked': checked, 'form': form}

        if request.POST.get("solve"):

            force = form.cleaned_data['force']

            game, grid = update_game(request, errors)

            if grid:

                save_grid = copy.deepcopy(grid)

                transcript = []

                solve_it(grid, force, transcript)

                jchange = json.dumps(json_squares(grid.changed))

                done, checked = check_answers(grid)

                dgrid = display(save_grid)

            context = {'game': game, 'errors':errors, 'changed': jchange, 'display':dgrid,
                       'done': done, 'checked': checked, 'form': form, 'transcript':transcript}

    else:

        if request.GET.get("error"):
            errors.append(request.GET.get("error"))

        if gid:
            game, grid, dgrid = get_game(gid, errors)

        form = GameForm()

        context = {'game': game, 'errors':errors, 'display':dgrid, 'form': form}

    return render(request, 'index.html', context)


@login_required
def games(request, gid=None):
    """ Create and update games """

    errors = []
    context = {}
    game = None

    if gid:
        try:
            game = Game.objects.get(id=gid)
        except ObjectDoesNotExist:
            errors.append('Game '+str(gid)+' not found')


    if request.method == 'POST':

        form = GamesForm(request.POST)

        if form.is_valid():
            level = form.cleaned_data['level']
            given = form.cleaned_data['given']
            note = form.cleaned_data['note']

            clean = check_given(given)

            if clean:
                if not game:
                    game = Game()
                    game.owner = request.user

                game.level = level
                game.given = clean
                game.note = note

                grid = Grid()
                grid.load(game)
                solve_it(grid, True)
                done, checked = check_answers(grid)

                if not done or not checked:
                    game.invalid = True
                    form.add_error('given', 'Invalid game provided!')
                else:
                    game.save()
                    return redirect('/games')


        errors.append('Form is not valid')

        context = {'errors':errors, 'form': form}

    else:

        if game:
            data = {'level': game.level, 'note': game.note, 'given': game.given}
            form = GamesForm(initial=data)
            context['game'] = game

        else:
            form = GamesForm()

        if request.GET.get("error"):
            form.fields["given"].errors = request.GET.get("error")

        if request.GET.get("given"):
            form.fields["given"].initial = request.GET.get("given")

        context['form'] = form

    kwargs = {}

    get_view_filters(request, 'game', kwargs)

    some = Game.objects.filter(**kwargs).order_by('level', 'id')

    context['games'] = some

    context['errors'] = errors

    return render(request, 'games.html', context)
