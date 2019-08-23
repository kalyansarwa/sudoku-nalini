""" Contains the few forms Sudoku uses """

from django import forms
from games.games import check_given
from games.models import Game


# LEVEL_CHOICES = (
#     ('1_easy', 'Easy'),
#     ('2_medium', 'Medium'),
#     ('3_hard', 'Hard'),
#     ('4_evil', 'Evil'),
#     )

COLOR_CHOICES = (
    ('green', 'green'),
    ('blue', 'blue'),
    ('purple', 'purple'),
    ('red', 'red'),
    ('orange', 'orange'),
    ('yellow', 'yellow')
    )


class GameForm(forms.Form):
    """ Controls when user is playing the game """

    level = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=Game.LEVEL_CHOICES,
                              initial="1_easy")

    pencil = forms.BooleanField(required=False, label="Allow Pencil Marks")
    hints = forms.BooleanField(required=False, label="Show Possibles")
    force = forms.BooleanField(required=False, label="Use brute force when solving")
    color = forms.BooleanField(required=False, label="Colors", initial=False)
    colors = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=COLOR_CHOICES,
                               initial=None)


class GamesForm(forms.Form):
    """ Controls when users is adding or modifying a game """

    level = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=Game.LEVEL_CHOICES,
                              initial="1_easy")
    note = forms.CharField(required=False, max_length=255)
    given = forms.CharField(min_length=81, label="Enter 81 digits, with 0s for blank squares",
                            widget=forms.Textarea(attrs={'rows': 9, 'cols': 18}))

    def clean(self):
        cdata = self.cleaned_data
        given = check_given(cdata.get('given'))

        if not given:
            self.add_error('given', "Wrong number of digits provided!")
        return cdata
