from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
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
            raise forms.ValidationError('Number must be 10 digits only')

        return data

    def clean_id_number(self):
        data = self.cleaned_data['id_number']

        if len(data) <= 6:
            raise forms.ValidationError('ID number must be more than 6 digits')

        return data

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your phone number'
        self.fields['phone_number'].help_text = ''

        self.fields['id_number'].widget.attrs['placeholder'] = 'Enter your ID number'
        self.fields['id_number'].help_text = ''


"""
form to change the users profile
"""


class EditProfileForm(UserChangeForm):
    password = None
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['first_name'].help_text = ''

        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['last_name'].help_text = ''
