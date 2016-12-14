from django.db import models

# Create your models here.
class Clipboard(models.Model) :
	hash_str = models.IntegerField(null = False)
	content = models.TextField(null = True)
	date_time = models.DateTimeField(null = False)
	int_time = models.IntegerField(null = False)
	valid_scope = models.IntegerField(null = False, default = 300)
	expire_date_time = models.IntegerField(null = False)
