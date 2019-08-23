""" This module has the views for people """

from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group


from .forms import RegisterForm

# Create your views here.


def register(request, gid=None):
    """ The base view of the game """

    errors = []
    context = {}

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if not form.is_valid():
            errors.append('Form is not valid')
            context = {'errors':errors, 'form': form}
            return render(request, 'register.html', context)

        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        repeat = form.cleaned_data['repeat']

        if password != repeat:
            errors.append('Passwords do not match')
            context = {'errors':errors, 'form': form}
            return render(request, 'register.html', context)

        try:
            newuser = User.objects.create_user(username, email, password)
            newuser.is_active = 1
            newuser.save()
        except Exception as ex:
            errors.append(str(ex))
            context = {'errors':errors, 'form': form}
            return render(request, 'register.html', context)

        try:
            group = Group.objects.get(name='player')
            newuser.groups.add(group)
        except ObjectDoesNotExist:
            pass


        newu = authenticate(username=newuser.username, password=password)

        if newu is not None and newu.is_active:
            login(request, newu)

        return redirect('/')
        #return render(request, 'index.html', context)

    form = RegisterForm()

    context = {'errors':errors, 'form': form}

    return render(request, 'register.html', context)
