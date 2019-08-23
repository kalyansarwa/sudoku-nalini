""" Admin for Games """

from django.contrib import admin

from .models import Game


class GameAdmin(admin.ModelAdmin):
    """ This class configures admin for Games """
    search_fields = ['level', 'owner', 'note']
    list_filter = ('level', 'shared')
    list_display = ('id', 'level', 'note', 'owner', 'given')
    ordering = ['level']

admin.site.register(Game, GameAdmin)
