from django import forms 
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput(attrs={'placeholder': 'Enter your password'}), validators=[validate_password])
    confirm_password = forms.CharField(widget= forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email
