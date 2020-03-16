from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

"""
form to register the user
"""


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'id_number', 'role')

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        if len(data) > 10:
            raise forms.ValidationError("Phone number must 10 characters only")
        elif len(data) < 10:
            raise forms.ValidationError("Phone number must be 10 characters only")
        return data

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your phone number'
        self.fields['phone_number'].helpt_text = '<small>Phone number must be 10 characters</small>'

        self.fields['id_number'].widget.attrs['placeholder'] = 'Enter your ID number'
        self.fields['id_number'].helpt_text = '<small>Id number must be 6 characters</small>'


"""
form for user registration
"""


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=50, strip=False)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

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

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'

        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['password1'].help_text = ' '

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        self.fields['password2'].help_text = ''
