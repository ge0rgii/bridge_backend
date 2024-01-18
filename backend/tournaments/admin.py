from django.contrib import admin

# Register your models here.

from .models import Tournament
admin.site.register(Tournament)

from .models import UserPoints
admin.site.register(UserPoints)