from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

"""
function for displaying the portal homepage when a user logs in
"""


def index_view(request):
    if request.user.is_authenticated:

        template_name = 'portal/index.html'
        message = 'Notice..You only have 4 days left to update your profile so that we can serve your better'
        context = {
            'message': message
        }

        return render(request, template_name, context)
    else:
        messages.warning(request, 'You have to login to access the portal')
        return redirect('login')
