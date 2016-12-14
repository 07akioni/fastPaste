import time

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from homePage import models

class Command(BaseCommand) :
	 def handle(self, *args, **options) :
		 now_time = timezone.now()
		 int_time = time.mktime(now_time.timetuple())
		 timeout_obj = models.Clipboard.objects.filter(expire_date_time__lte = int_time)
		 timeout_obj.delete()
