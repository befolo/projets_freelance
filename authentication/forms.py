from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=63, label='email')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')
