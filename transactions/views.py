from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
import requests
from requests import auth
import json
from django.contrib import messages

import requests,json
from requests import auth
me = auth.HTTPDigestAuth("admin", "admin")
resp = requests.get("http://51.132.8.252:8060/v1/search?format=json", auth=me)
jsonFile = json.loads(resp.text)
result = jsonFile["results"]
a=[]
for key in result:
    uri = key["uri"]
    res = requests.get("http://51.132.8.252:8060/v1/documents?uri=" + uri, auth = me)
    a.append(res.json())
print(a)
 
a = [
	{'accounts': [
		{'id': '8ca8a7e4-6d02-40e3-a129-0b2bf89de9f0',
		'label': 'My Account',
		'bank_id': 'GENODEM1GLS',
		'account_routings': [
			{'scheme': 'accountNumber',
			'address': '123456'}
			],
		'balance': 
			{'currency': 'EUR',
			'amount': '100' }
		}
	], 'overall_balance': 
			{'currency': 'EUR',
			'amount': '100'},
		'overall_balance_date': '2017-09-19T00:00:00Z'}
]



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

@login_required
def transactions(request):
	return render(request, 'transactions/transactions.html')

@login_required
def report(request):
	return render(request, 'transactions/report.html')