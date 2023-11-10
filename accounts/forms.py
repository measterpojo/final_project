from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    AuthenticationForm)

from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'phone', 'date_of_birth', 'password')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'phone', 'date_of_birth', 'is_staff', 'is_superuser')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'phone', 'date_of_birth', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]


class LoginForm(AuthenticationForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=50, required=True)

    remeber_me = forms.BooleanField(required=True)

    class Meta:
        model = CustomUser

