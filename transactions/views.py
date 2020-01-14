from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
import requests
from requests import auth
from django.contrib import messages
from django.core.mail import send_mail
from . forms import ContactForm
import requests,json, urllib

me = auth.HTTPDigestAuth("admin", "admin")

def getRows(userID):
	row = []
	transactionAttributes = ["BookingDateTime", "TransactionInformation", "Amount", "Currency"]
	id = str(userID)
	res = requests.get("http://51.132.8.252:8060/v1/documents?uri=/documents/" + id +".json", auth = me)
	if (res.status_code == 404):
		return False
	a = json.loads(res.text)
	for transaction in a['Data']['Transaction']:
		collecting = {
			'BookingDateTime': '',
			'TransactionInformation': '',
			'Amount': '',
			'Currency': ''
		}
		for attribute in transactionAttributes:
			if ((attribute == "Amount") or (attribute == "Currency")) :
				collecting[attribute] = transaction['Amount'][str(attribute)]
			else:
				collecting[attribute] = transaction[str(attribute)]
		row.append(collecting)
	return row

@login_required
def home(request):
	request.session.set_expiry(600)
	if (getRows(request.user.profile.userID) == False):
		context = {
			'rows': [{
			'BookingDateTime': 'No Data Found',
			'TransactionInformation': 'Incorrect UserID linked',
			'Amount': 'Update userID',
			'Currency': 'and try again'
			}]
		}
		return render(request, 'transactions/home.html', context)
	context = {
		'rows': getRows(request.user.profile.userID)
	}
	return render(request, 'transactions/home.html', context)

@login_required
def profile(request):
	request.session.set_expiry(600)
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
	request.session.set_expiry(600)
	if (getRows(request.user.profile.userID) == False):
		context = {
			'rows': [{
			'BookingDateTime': 'No Data Found',
			'TransactionInformation': 'Incorrect UserID linked',
			'Amount': 'Update userID and try again'
			}]
		}
		return render(request, 'transactions/transactions.html', context)
	context = {
		'rows': getRows(request.user.profile.userID)
	}
	return render(request, 'transactions/transactions.html', context)

@login_required
def report(request):
	request.session.set_expiry(600)
	return render(request, 'transactions/report.html')

@login_required
def help(request):
	request.session.set_expiry(600)
	if request.method == "POST":
		form = ContactForm(request.POST)
		if form.is_valid:
			form.save()
			messages.success(request, f'Message sent!')
			send_mail(form.cleaned_data.get('subject'), form.cleaned_data.get('message')+"\n\n Reply to: "+form.cleaned_data.get('email'), 'pwresetst45@gmail.com', ['pwresetst45@gmail.com'])
			return redirect('home')
	else:
		form = ContactForm()
	context = {
		'form' : form
	}
	return render(request, 'transactions/help.html', context)