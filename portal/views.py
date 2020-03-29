from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import EditProfileForm, UserProfileForm, AddTown

"""
function for displaying the portal homepage when a user logs in
"""


@login_required
def index_view(request):
    if request.user.is_authenticated:

        template_name = 'portal/index.html'

        return render(request, template_name, {})
    else:
        messages.warning(request, 'You have to login to access the portal')
        return redirect('login')


"""
function to edit the user profile
"""


@login_required
def edit_profile_view(request):
    template_name = 'portal/edit_profile.html'
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(request.POST, instance=request.user.profile)
            town_form = AddTown(request.POST)

            if form.is_valid() and profile_form.is_valid() and town_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.is_profile = True
                profile.save()
                form.save()
                town_form.save()

                messages.success(request, 'Details updated successfully')
                return redirect('portal')
        else:
            form = EditProfileForm(instance=request.user)
            profile_form = UserProfileForm(instance=request.user.profile)
            town_form = AddTown()
    else:
        messages.error(request, 'you must be logged in')
        return redirect('login')

    context = {
        'user_form': form,
        'profile_form': profile_form,
        'town_form': town_form
    }

    return render(request, template_name, context)
