from django.urls import path 
from . import views 

urlpatterns = [
path('accounts/', views.AccountListCreate.as_view()),
path('tournaments/', views.TournamentList.as_view()),
path('signup/', views.signup),
path('login/', views.login),
path('change-password/', views.change_password),
path('userpoints/<int:tournament_id>/', views.UserPointsList.as_view()),
path('tournaments/<int:pk>/', views.TournamentView.as_view()),

]