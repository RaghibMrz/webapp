from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
import requests
from requests import auth
import json
from django.contrib import messages

# me = auth.HTTPDigestAuth("admin", "admin")
# resp = requests.get("https://team45resourcesdiag.blob.core.windows.net/bootdiagnostics-mlteam45-ed961ad5-34f2-4417-86af-a77c432a0c81/balance-test.json", auth=me)
# datas = json.loads(resp.text)

db = [
	{
		'fName': 'Raghib',
		'sName': 'Mirza',
		'mName': 'n/a',
		'balance': '£5,000'
	},
	{
		'fName': 'Other',
		'sName': 'Person',
		'mName': 'Middle',
		'balance': '£5,000,000'
	},
]

@login_required
def home(request):
	context = {
		'db': db
	}
	return render(request, 'transactions/home.html', context)

@login_required
def profile(request):
	if request.method == 'POST':
		uForm = UserUpdateForm(request.POST, request.FILES, instance=request.user)
		pForm = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if uForm.is_valid() and pForm.is_valid():
			uForm.save()
			pForm.save()
			messages.success(request, f'Account successfully updated')
			return redirect('profile')
	#return statement in line above is to prevent user from falling to line below
	#phenomenon called 'get-redirect pattern'- when u reload browser afrer submitting data
	#post request will be duplicated.
	else:
		uForm = UserUpdateForm(instance=request.user)
		pForm = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'uForm': uForm,
		'pForm': pForm,
	}
	return render(request, 'transactions/profile.html', context)