from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField()
	firstname = forms.CharField(max_length=30, help_text='First Name')
	lastname = forms.CharField(max_length=30, help_text='Last Name')

	class Meta:
		model = User
		fields = ['firstname', 'lastname', 'username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	firstname = forms.CharField(max_length=30, help_text='First Name')
	lastname = forms.CharField(max_length=30, help_text='Last Name')

	class Meta:
		model = User
		fields = ['firstname', 'lastname', 'username', 'email']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['img']