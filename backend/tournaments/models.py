from django.db import models

# Create your models here.

from django.contrib.auth.models import User
class Tournament(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserPoints(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    deals = models.IntegerField(default=1)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + " " + self.tournament.name


    

