from django.shortcuts import render
import requests
from requests import auth
import json


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

def home(request):
	context = {
		'db': db
	}
	return render(request, 'transactions/home.html', context)
