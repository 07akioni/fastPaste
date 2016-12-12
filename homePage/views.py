import random

from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from homePage import models


# Create your views here.
def welcome(request) :
	return render(request, 'home.html')

def new_clipboard(request) :
	print('new_clipboard')
	hash_str = str(random.randint(10000, 100000))
	clipBoard = models.Clipboard(hash_str = hash_str, date_time = timezone.now())
	clipBoard.save()
	return HttpResponseRedirect('/clipboard/' + hash_str)

def clipBoard(request, hash_str) :
	context = {}
	clipboard = models.Clipboard.objects.get(hash_str = hash_str)
	context['clipboard'] = clipboard
	# print(context)
	# return HttpResponse('What the fuck?')
	return render(request, 'clipboard.html', context = context)

def get_clipboard(request) :
	context = {}
	hash_str = request.GET['hash_str']
	return HttpResponseRedirect('/clipboard/' + hash_str)

def save_clipboard(request) :
	hash_str = request.POST['id']
	content = request.POST['content']
	clipboard = models.Clipboard.objects.get(hash_str = hash_str)
	clipboard.content = content
	clipboard.save()
	return HttpResponseRedirect('/clipboard/' + hash_str)
