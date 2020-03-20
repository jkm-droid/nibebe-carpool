from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import EditProfileForm, UserProfileForm

"""
function for displaying the portal homepage when a user logs in
"""


def index_view(request):
    if request.user.is_authenticated:

        template_name = 'portal/index.html'

        context = {

        }

        return render(request, template_name, context)
    else:
        messages.warning(request, 'You have to login to access the portal')
        return redirect('login')


"""
function to edit the user profile
"""


def edit_profile_view(request):
    template_name = 'portal/edit_profile.html'
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(request.POST, instance=request.user.profile)

            if form.is_valid() and profile_form.is_valid():
                form.save()
                profile_form.save()
                messages.success(request, 'Details updated successfully')
                return redirect('portal')
        else:
            form = EditProfileForm(instance=request.user)
            profile_form = UserProfileForm(instance=request.user.profile)
    else:
        messages.error(request, 'you must be logged in')
        return redirect('login')

    context = {
        'user_form': form,
        'profile_form': profile_form
    }

    return render(request, template_name, context)
