""" This module contains people related models """

from django.db import models
from django.contrib.auth.models import User



# This is the basic Peple class to store additions to User
class Person(models.Model):
    """ Model class for Person """

    id = models.AutoField(primary_key=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)

    def get_fields(self):
        """ return field values array """
        return [(field.name, field.value_to_string(self)) for field in Person._meta.fields]

    @classmethod
    def get_field_names(cls):
        """ return field names only array """
        return [field.name for field in cls._meta.fields]

    def __str__(self):
        """ return string representation """
        return 'Person: (' + str(self.id)+') ' + str(self.user.email)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
        db_table = "people"
        managed = True
        permissions = (
            ("view_own", "Can view self"),
            ("view", "Can view any person"),
        )
