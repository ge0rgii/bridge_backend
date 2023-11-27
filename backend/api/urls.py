from django.urls import path 
from . import views 

urlpatterns = [
path('accounts/', views.AccountListCreate.as_view()), 
path('signup/', views.signup),
path('login/', views.signup),
]