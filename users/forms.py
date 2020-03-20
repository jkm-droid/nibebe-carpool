from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


"""
form for user registration
"""


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=50, strip=False)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_username(self):
        data = self.cleaned_data['username']
        if len(data) <= 4:
            raise forms.ValidationError("Too short.Username must be more than 5 characters")
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        email_exists = User.objects.filter(email=data)

        if email_exists.exists():
            raise forms.ValidationError("Email address already exists!")
        return data

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['placeholder'] = 'Enter email address'
        self.fields['email'].help_text = ''

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        self.fields['username'].help_text = ' '

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['password1'].help_text = ' '

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        self.fields['password2'].help_text = ''
