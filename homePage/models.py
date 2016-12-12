from django.db import models

# Create your models here.
class Clipboard(models.Model) :
	hash_str = models.IntegerField(null = False)
	content = models.TextField(null = True)
	date_time = models.DateTimeField(null = False)
