""" Contains the registration form """

from django import forms


class RegisterForm(forms.Form):
    """ Controls when user is playing the game """

    username = forms.CharField(required=True, max_length=255, label='Username:')
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label='Password:')
    repeat = forms.CharField(widget=forms.PasswordInput, label='Retype password:')
