from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.forms.widgets import TextInput, PasswordInput
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """
    Form for user registration.
    It inherits from Django's UserCreationForm.
    """
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.', widget=forms.EmailInput())
    first_name = forms.CharField(max_length=254, required=False, help_text='Name you has entered will be used for visit confirmation.', widget=forms.TextInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2', )
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class MyLoginForm(AuthenticationForm):
    """
    Form for user authentication.
    It inherits from Django's AuthenticationForm.
    """
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'})


class MyPasswordResetForm(PasswordResetForm):
    """
    Form for password reset.
    It inherits from Django's PasswordResetForm.
    """
    def __init__(self, *args, **kwargs):
        super(MyPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})


class MySetPasswordForm(SetPasswordForm):
    """
    Form for setting a new password.
    It inherits from Django's SetPasswordForm.
    """
    def __init__(self, *args, **kwargs):
        super(MySetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New password confirmation'})
