import random
import json
import time

from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from homePage import models
from django.utils import timezone


# Create your views here.
def welcome(request) :
	context = {}
	try :
		referer = request.META['HTTP_REFERER']
		# return HttpResponse(referer)
		tmp = referer.split('/clipboard/')
		print(tmp)
		if len(tmp) == 2 :
			hash_str = tmp[1]
			if hash_str.isdigit() :
				context['hash_str'] = int(hash_str)
			else :
				tmp = tmp[1].split('?hash_str=')
				print(tmp)
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
		# return HttpResponse("???")
		return render(request, 'home.html', context = context)

def new_clipboard(request) :
	count = 20
	while count > 0 :
		hash_str = str(random.randint(10000, 100000))
		try :
			count -= 1
			models.Clipboard.objects.get(hash_str = hash_str)
		except models.Clipboard.DoesNotExist :
			now_time = timezone.now()
			int_time = time.mktime(now_time.timetuple())
			clipBoard = models.Clipboard(hash_str = hash_str, date_time = now_time, int_time = int_time, expire_date_time = int_time + 300)
			clipBoard.save()
			return HttpResponseRedirect('/clipboard/' + hash_str)
	context = {}
	context['error_mesg'] = '剪贴板太多 网站装不下了'
	return render(request, 'notfindclipboard.html', context)

def clipBoard(request, hash_str) :
	context = {}
	if hash_str == '':
		try :
			hash_str = request.GET['hash_str']
		except Exception :
			context['error_mesg'] = '未找到剪贴板'
			return render(request, 'notfindclipboard.html', context = context)
	if hash_str == '':
		context['error_mesg'] = '搜索不能为空'
		return render(request, 'notfindclipboard.html', context = context)
	try :
		clipboard = models.Clipboard.objects.get(hash_str = hash_str)
		context['clipboard'] = clipboard
		context['lefttime'] = int(clipboard.expire_date_time - time.mktime(timezone.now().timetuple()))
		if(context['lefttime'] < 0) :
		 	context['lefttime'] = 0
		return render(request, 'clipboard.html', context = context)
	except models.Clipboard.DoesNotExist:
		context['hash_str'] = hash_str
		return render(request, 'notfindclipboard.html', context = context)
	except ValueError :
		context['error_mesg'] = '剪贴板编号仅能由数字构成'
		return render(request, 'notfindclipboard.html', context = context)

def get_clipboard(request, hash_str) :
	context = {}
	try :
		clipboard = models.Clipboard.objects.get(hash_str = hash_str)
		if clipboard.content == None :
			clipboard.content = ''
		context['content'] = clipboard.content
		return HttpResponse(json.dumps(context), content_type = 'text/json')
	except models.Clipboard.DoesNotExist :
		context['status'] = 'failed'
		return HttpResponse(json.dumps(context), content_type = 'text/json')
	except ValueError :
		context['status'] = 'failed'
		return HttpResponse(json.dumps(context), content_type = 'text/json')

def post_clipboard(request) :
	if request.method == 'POST' :
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

def add_max_scope(request) :
	if request.method == 'POST' :
		try :
			hash_str = request.POST['hash_str']
			add_time = int(request.POST['add_time'])
			clipboard = models.Clipboard.objects.get(hash_str = hash_str)
			if clipboard.valid_scope >= clipboard.max_valid_scope :
				context = {'status' : 'failed', 'info' : "max"}
				return HttpResponse(json.dumps(context), content_type = 'text/json')
			if clipboard.valid_scope + add_time < clipboard.max_valid_scope :
				clipboard.expire_date_time += add_time
				clipboard.valid_scope += add_time
				clipboard.save()
				context = {'status' : 'success', 'info' : "none", 'add_time' : add_time}
				return HttpResponse(json.dumps(context), content_type = 'text/json')
			elif clipboard.valid_scope + add_time >= clipboard.max_valid_scope :
				clipboard.expire_date_time += (clipboard.max_valid_scope - clipboard.valid_scope)
				context = {'status' : 'success', 'info' : "none", 'add_time' : (clipboard.max_valid_scope - clipboard.valid_scope)}
				clipboard.valid_scope = clipboard.max_valid_scope
				clipboard.save()
				return HttpResponse(json.dumps(context), content_type = 'text/json')
			else :
				context = {'status' : 'failed', 'info' : "none"}
				return HttpResponse(json.dumps(context), content_type = 'text/json')
		except:
			context = {'status' : 'failed', 'info' : 'none'}
			return HttpResponse(json.dumps(context), content_type = 'text/json')
	else :
		context = {'status' : 'failed', info: 'none'}
		return HttpResponse(json.dumps(context), content_type = 'text/json')

def not_found(request) :
	context = {}
	context['error_mesg'] = '你访问的页面不存在'
	return render(request, 'notfindclipboard.html', context = context)
