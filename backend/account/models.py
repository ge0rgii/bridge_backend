from django.db import models

# Create your models here.

from django.contrib.auth.models import User
class Account(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE) 
	avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
	def __str__(self):
		return self.user.username
