from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from .forms import SignUpForm, MyLoginForm, MyPasswordResetForm, MySetPasswordForm
from django.contrib.auth import login


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


class MyLoginView(LoginView):
    form_class = MyLoginForm
    template_name = 'registration/login.html'


class MyPasswordResetView(PasswordResetView):
    form_class = MyPasswordResetForm
    template_name = 'registration/password_reset.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = MySetPasswordForm
    template_name = 'registration/password_reset_confirm.html'
