""" Tests Sudoku people functions """

from django.test import TestCase
from django.contrib.auth.models import User, Group

# Create your tests here.

class PersonTestCase(TestCase):
    """ Test Person """

    def setUp(self):

        Group.objects.bulk_create([Group(name=u'player'), Group(name=u'admin')])


    def test_person(self):
        """ Test person Creation """

        newuser = User.objects.create_user('testytest', 'testy@tests.com', 'badpass')

        newuser.is_active = 1
        newuser.save()

        group = Group.objects.get(name='player')
        newuser.groups.add(group)

        self.assertIsNotNone(newuser)
