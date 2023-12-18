from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from .serializers import AccountSerializer 
from account.models import Account
class AccountListCreate(generics.ListCreateAPIView):
	serializer_class = AccountSerializer
	permission_classes = [permissions.IsAuthenticated]
	def get_queryset(self):
		user = self.request.user
		return Account.objects.filter(user=user)
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signup(request):
	if request.method == 'POST': 
		try:
			data = JSONParser().parse(request) # data is a dictionary 
			user = User.objects.create_user(username=data['username'], \
				password=data['password'])
			token = Token.objects.create(user=user)
			return JsonResponse({'token':str(token)}, status=201) 
		except IntegrityError:
			return JsonResponse( \
			{'error':'username taken. choose another username'}, status=400)

from django.contrib.auth import authenticate

@csrf_exempt
def login(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		user = authenticate(username=data['username'], \
			password=data['password']) 
		if user is None:
			return JsonResponse( \
				{'error':'unable to login. check username and password'}, status=400)
		else: 
			try:
				token = Token.objects.get(user=user)
			except: 
				token = Token.objects.create(user=user)
			return JsonResponse({'token':str(token)}, status=201)

@csrf_exempt
def change_password(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		user = authenticate(username=data['username'], \
			password=data['password']) 
		if user is None:
			return JsonResponse( \
				{'error':'unable to authenticate. check old password'}, status=400)
		else: 
			try:
				user.set_password(data['new_password'])
				user.save()
				return JsonResponse({'message':'password changed'}, status=201)
			except: 
				return JsonResponse( \
				{'error':'unable to change password'}, status=400)
			
			




