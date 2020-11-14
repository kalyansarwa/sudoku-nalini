""" This module contains permissions classes for games to check game access
    by group and/or owner."""

from django.core.exceptions import ObjectDoesNotExist
#from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


def get_user_permissions(user, content_type):
    """ Fetch all request.user permissions """

    if user.is_superuser:
        perms = Permission.objects.filter(content_type=content_type)

    perms = user.user_permissions.filter(content_type=content_type) | \
        Permission.objects.filter(group__user=user, content_type=content_type)
    perm_codes = []

    for perm in perms:
        perm_codes.append(perm.codename)

    return perm_codes



def get_view_filters(request, model, kwargs):
    """ provide filters to screen what user can see """

    if not request.user.is_authenticated:
        kwargs['id'] = -1
        return

    try:
        ctype = ContentType.objects.get(model=model)
    except ObjectDoesNotExist:
        kwargs['id'] = -1
        return


    perms = get_user_permissions(request.user, ctype.id)

    if not perms:
        kwargs['id'] = -1
        return

    if 'view' in perms:
        return

    # check for ownership
    if 'view_own' in perms:
        kwargs['owner'] = request.user.id

    else:
        kwargs['id'] = -1

    return
