from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField()
	firstname = forms.CharField(max_length=30)
	lastname = forms.CharField(max_length=30)

	class Meta:
		model = User
		fields = ['firstname', 'lastname', 'username', 'email', 'password1', 'password2']