import random
import json

from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from homePage import models


# Create your views here.
def welcome(request) :
	context = {}
	try :
		referer = request.META['HTTP_REFERER']
		tmp = referer.split('/clipboard/')
		if len(tmp) == 2 :
			hash_str = tmp[1]
			if hash_str.isdigit() :
				context['hash_str'] = int(hash_str)
			else :
				tmp = tmp[1].split('?hash_str=')
				if len(tmp) == 2 :
					hash_str = tmp[1]
					if hash_str.isdigit() :
						context['hash_str'] = int(hash_str)
		if context['hash_str'] is not None :
			try :
				models.Clipboard.objects.get(hash_str = context['hash_str'])
			except models.Clipboard.DoesNotExist:
				context['hash_str'] = None;
		return render(request, 'home.html', context = context)
	except KeyError:
		return render(request, 'home.html', context = context)

def new_clipboard(request) :
	count = 20
	while count > 0 :
		hash_str = str(random.randint(10000, 100000))
		try :
			count -= 1
			models.Clipboard.objects.get(hash_str = hash_str)
		except models.Clipboard.DoesNotExist :
			clipBoard = models.Clipboard(hash_str = hash_str, date_time = timezone.now())
			clipBoard.save()
			return HttpResponseRedirect('/clipboard/' + hash_str)
	context = {}
	context['error_mesg'] = '剪贴板太多 网站装不下了'
	return render(request, 'notfindclipboard.html', context)

def clipBoard(request, hash_str) :
	context = {}
	if hash_str == '':
		hash_str = request.GET['hash_str']
	if hash_str == '':
		context['error_mesg'] = '搜索不能为空'
		return render(request, 'notfindclipboard.html', context = context)
	try :
		clipboard = models.Clipboard.objects.get(hash_str = hash_str)
		context['clipboard'] = clipboard
		return render(request, 'clipboard.html', context = context)
	except models.Clipboard.DoesNotExist:
		context['hash_str'] = hash_str
		return render(request, 'notfindclipboard.html', context = context)

def get_clipboard(request, hash_str) :
	context = {}
	try :
		clipboard = models.Clipboard.objects.get(hash_str = hash_str)
		if clipboard.content == None :
			clipboard.content = ''
		context['content'] = clipboard.content
		print(json.dumps(context))
		return HttpResponse(json.dumps(context), content_type = 'text/json')
	except models.Clipboard.DoesNotExist :
		context['hash_str'] = hash_str
		return render(request, 'notfindclipboard.html', context = context)

def post_clipboard(request) :
	if method == 'POST' :
		try :
			hash_str = request.POST['hash_str']
			content = request.POST['content']
			clipboard = models.Clipboard.objects.get(hash_str = hash_str)
			clipboard.content = content
			clipboard.save()
			context = {'status' : 'success'}
			return HttpResponse(json.dumps(context), content_type = 'text/json')
		except:
			context = {'status' : 'failed'}
			return HttpResponse(json.dumps(context), content_type = 'text/json')
	else :
		context = {'status' : 'failed'}
		return HttpResponse(json.dumps(context), content_type = 'text/json')