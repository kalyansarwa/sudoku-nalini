""" This module contains game related models """
import re
import copy


from django.db import models
from django.contrib.auth.models import User


# This is the basic Game class to store the games
class Game(models.Model):
    """ Model class for Game """

    LEVEL_CHOICES = (
        ('1_easy', 'Easy'),
        ('2_medium', 'Medium'),
        ('3_hard', 'Hard'),
        ('4_evil', 'Evil'),
        )

    id = models.AutoField(primary_key=True, blank=True)
    level = models.CharField(max_length=25, choices=LEVEL_CHOICES, default='hard',
                             null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    given = models.TextField(null=True, blank=True)
    shared = models.BooleanField(default=False)
    invalid = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def get_fields(self):
        """ return field values array """
        return [(field.name, field.value_to_string(self)) for field in Game._meta.fields]

    @classmethod
    def get_field_names(cls):
        """ return field names only array """
        return [field.name for field in cls._meta.fields]

    def __str__(self):
        """ return string representation """
        return 'Game: (' + str(self.id)+') ' + str(self.level) + ': ' + self.given

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'
        db_table = "games"
        managed = True
        permissions = (
            ("view_own", "Can view own game"),
            ("view", "Can view any game"),
            ("play_any", "Can play any game"),
            ("change_own", "Can change own game"),
            ("delete_own", "Can delete own game"),
        )

# Memory Only Classes


class Square():
    """ class for an individual square """

    def __init__(self, row, col, val=None):

        self.row = row
        self.col = col
        self.pencil = ""
        self.color = None
        self.wrong = False

        if val:
            self.answer = val
            self.starter = 1
            self.possibles = [val]
        else:
            self.answer = None
            self.starter = 0
            self.possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __str__(self):
        return '['+str(self.row)+']['+str(self.col)+']='+str(ifnull(self.answer, 0))+ \
            ' p='+str(self.possibles)


    def not_possible(self, grid, vals, solve=False):
        """ remove stuff not possible """

        for val in vals:
            if val == self.answer:
                # throw an exception?
                self.wrong = True
                grid.errors += 1
                return False
            if val in self.possibles:
                #print('Updating square '+str(self))
                if not solve:
                    self.possibles.remove(val)
                else:
                    ucopy = copy.deepcopy(self)
                    self.possibles.remove(val)
                    if len(self.possibles) == 1:
                        self.answer = self.possibles[0]
                        grid.solved += 1
                    rcopy = copy.deepcopy(self)
                    grid.changed.append(rcopy)
                #print('Now its '+str(self))

        return True


    def set_answer(self, grid, val, solve=False):
        """ set the answer """

        if solve:
            if not self.answer:
                grid.solved += 1
            ucopy = copy.deepcopy(self)
        self.possibles = [val]
        self.answer = val
        if solve:
            rcopy = copy.deepcopy(self)
            grid.changed.append(rcopy)



    def match_some(self, vals):
        """ Return true if the vals are the only thing in possibles """

        if len(vals) != len(self.possibles):
            return False

        for val in vals:
            if val not in self.possibles:
                return False
        return True

    def as_json(self):
        """ return square as json """
        return dict(row=self.row, col=self.col, possible=self.possibles, answer=self.answer,
                    wrong=self.wrong, pencil=self.pencil, starter=self.starter)



class Grid():
    """ class for the grid """

    def __init__(self):

        self.solved = 0
        self.errors = 0
        self.level = None
        self.changed = []
        self.transcript = []

        self.grid = [[], [], [], [], [], [], [], [], []]


    def load(self, game):
        """ Load the working grid from the game object """

        digits = re.compile('[1-9]')

        col = 0
        row = 0

        for i in range(0, len(game.given)):
            if game.given[i] == '0':
                self.grid[row].append(Square(row, col))
                col += 1
            elif digits.search(game.given[i]) is not None:
                self.solved += 1
                self.grid[row].append(Square(row, col, int(game.given[i])))
                col += 1

            if col > 8:
                col = 0
                row += 1

            if row > 8:
                return


    def print(self):
        """ Print the working grid from the game object """

        print('Solved='+str(self.solved))
        boundary = '+---+---+---+---+---+---+---+---+---+'

        print(boundary)

        for row in self.grid:
            line = '|'
            for col in row:
                if col.answer:
                    line += ' '+str(col.answer)+' |'
                else:
                    line += '   |'

            print(line)
            print(boundary)



def ifnull(val1, val2):
    """ mimics SQL IFNULL function """
    if val1:
        return val1
    return val2
