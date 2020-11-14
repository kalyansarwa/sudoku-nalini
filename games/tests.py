""" Tests Sudoku game functions """

from django.test import TestCase
from django.contrib.auth.models import User

from games.models import Game, Grid
from games.games import update_possibles, check_answers, solve_it

# Create your tests here.

class SimpleTestCase(TestCase):
    """ Test Easy Sudoku """


    def setUp(self):
        """ Test Game Creation """
        User.objects.create(first_name='Testy', last_name='Test', username='testytest',
                            email='testy@tests.com')
        people = User.objects.filter(username='testytest')
        if people:
            person = people[0]

        easy = """000 780 930 012 953 600 070 006 000
                  046 800 002 500 000 006 200 004 780
                  000 300 060 003 679 450 068 045 000"""

        Game.objects.create(level='1_easy', note='Easy', shared=1, given=easy, owner=person)

        hard = """900 000 008 002 010 050 037 004 900
                  000 003 400 090 060 010 004 500 000
                  003 200 570 010 050 300 700 000 006"""

        xywing = """000 000 000 000 107 008 070 392 541
                    004 000 092 005 000 600 930 000 400
                    192 785 060 500 403 000 000 000 000"""

        xwing = """500 000 003 004 302 900 090 010 080
                   040 030 090 008 407 600 070 080 020
                   010 070 050 009 501 700 400 000 002"""

        Game.objects.create(level='1_easy', note='Easy', shared=1, given=easy, owner=person)
        Game.objects.create(level='4_evil', note='Hard', shared=1, given=hard, owner=person)
        Game.objects.create(level='4_evil', note='Xwing', shared=1, given=xwing, owner=person)
        Game.objects.create(level='4_evil', note='XYwing', shared=1, given=xywing, owner=person)



    def test_game(self):
        """ Test Game Solution """

        game = None

        games = Game.objects.filter(note='Easy')
        if games:
            game = games[0]

        self.assertIsNotNone(game)

        transcript = []
        errors = []

        if game:

            grid = Grid()
            grid.load(game)
            self.assertIsNotNone(grid)

            update_possibles(grid, errors)

            self.assertEqual(errors, [])

            if grid:

                transcript = []

                solve_it(grid, True, transcript)

                done, checked = check_answers(grid)

                self.assertTrue(done)
                print('checked='+str(checked))
                self.assertEqual(checked, 1)

                print(transcript)

                self.assertEqual(transcript,
                                 ['Used rule only_me', 'Used rule not_me', 'Solved the puzzle!!'])


    def test_hard(self):
        """ Test Game Solution """

        game = None

        games = Game.objects.filter(note='hard')
        if games:
            game = games[0]

        self.assertIsNotNone(game)

        transcript = []
        errors = []

        if game:

            grid = Grid()
            grid.load(game)
            self.assertIsNotNone(grid)

            update_possibles(grid, errors)

            self.assertEqual(errors, [])

            if grid:

                transcript = []

                solve_it(grid, True, transcript)

                done, checked = check_answers(grid)

                self.assertTrue(done)

                print('checked='+str(checked))
                self.assertEqual(checked, 1)

                print(transcript)

                self.assertEqual(transcript,
                                 ['Used rule only_me', 'Used rule not_me', 'Used rule blockers',
                                  'Used rule hidden_twins', 'Used rule hidden_triplets',
                                  'Used rule colors', 'Used rule swordfish', 'Solved the puzzle!!'])



    def test_xwing(self):
        """ Test Game Solution """

        game = None

        games = Game.objects.filter(note='Xwing')
        if games:
            game = games[0]

        self.assertIsNotNone(game)

        transcript = []
        errors = []

        if game:

            grid = Grid()
            grid.load(game)
            self.assertIsNotNone(grid)

            update_possibles(grid, errors)

            self.assertEqual(errors, [])

            if grid:

                transcript = []

                solve_it(grid, True, transcript)

                done, checked = check_answers(grid)

                self.assertTrue(done)

                print('checked='+str(checked))
                self.assertEqual(checked, 1)

                print(transcript)

                self.assertEqual(transcript,
                                 ['Used rule only_me', 'Used rule not_me', 'Used rule blockers',
                                  'Used rule xwing', 'Used rule hidden_quads', 'Used rule twins',
                                  'Solved the puzzle!!'])



    def test_xywing(self):
        """ Test Game Solution """

        game = None

        games = Game.objects.filter(note='XYwing')
        if games:
            game = games[0]

        self.assertIsNotNone(game)

        transcript = []
        errors = []

        if game:

            grid = Grid()
            grid.load(game)
            self.assertIsNotNone(grid)

            update_possibles(grid, errors)

            self.assertEqual(errors, [])

            if grid:

                transcript = []

                solve_it(grid, True, transcript)

                done, checked = check_answers(grid)

                self.assertTrue(done)

                print('checked='+str(checked))
                self.assertEqual(checked, 1)

                print(transcript)

                self.assertEqual(transcript,
                                 ['Used rule only_me', 'Used rule not_me', 'Used rule blockers',
                                  'Used rule xywing', 'Solved the puzzle!!'])
