from django.db import models

# Create your models here.

from django.contrib.auth.models import User
class Account(models.Model):
	first_name = models.CharField(max_length=20) 
	last_name = models.CharField(max_length=20)
	user = models.ForeignKey(User, on_delete=models.CASCADE) 
	def __str__(self):
		return self.first_name
