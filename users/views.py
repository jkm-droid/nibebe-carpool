from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import EmailMessage
from .token_generator import account_activation_token

"""
function for registering users
"""


def register_user_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered')
        return redirect('portal')
    else:
        form = UserRegistrationForm()

        if request.method == "POST":
            form = UserRegistrationForm(request.POST)

            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_subject = "Nibebe Carpool Account Activation"
                # preparing the email message
                email_message = render_to_string('users/activate_account.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                print("----------------" + email_message + "-------------------")
                user_email = form.cleaned_data['email']
                email = EmailMessage(email_subject, email_message, to=[user_email])
                email.send()

                messages.info(request, f"Registered successfully. Visit {user_email} to confirm your email")
                return redirect('/users/login')
        else:
            form = UserRegistrationForm()

        template_name = 'users/register.html'
        context = {
            'form': form,
        }

        return render(request, template_name, context)


"""
function to activate the user's account after registering
"""


def activate_account_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        messages.info(request, 'Account Activated successfully...Login to access your account')
        return redirect('login')
    else:
        return HttpResponse('Invalid token')


"""
function to log user in the portal
"""


def login_user_view(request):
    template_name = 'users/login.html'

    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('portal')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"Successfully logged in as {username}")
                return redirect('portal')
            else:
                messages.warning(request, "Wrong Username/Password")
                return redirect('/users/login')
        else:
            return render(request, template_name, {})


"""
function to logout user
"""


def logout_user_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'Successfully logged out!!!')
        return redirect('login')
    else:
        messages.info(request, 'You are logged out..Please login ')
        return redirect('login')
