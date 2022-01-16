from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def monit(request):
	return HttpResponse('Gunicorn is working!!')
