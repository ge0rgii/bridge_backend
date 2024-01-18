from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

# Create your views here.

from rest_framework import generics, permissions
from .serializers import AccountSerializer 
from account.models import Account
from django.views.decorators.csrf import csrf_exempt
class AccountListCreate(generics.ListCreateAPIView):
	serializer_class = AccountSerializer
	permission_classes = [permissions.IsAuthenticated]
	def get_queryset(self):
		user = self.request.user
		return Account.objects.filter(user=user)
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

from .serializers import TournamentSerializer
from tournaments.models import Tournament
class TournamentList(generics.ListAPIView):
	serializer_class = TournamentSerializer
	permission_classes = [permissions.IsAuthenticated]
	def get_queryset(self):
		return Tournament.objects.all()

class TournamentView(generics.RetrieveAPIView):
	permission_classes = [permissions.IsAuthenticated]
	queryset = Tournament.objects.all()
	serializer_class = TournamentSerializer

from tournaments.models import UserPoints
from .serializers import UserPointsSerializer
from .serializers import UserPointsSerializer1

class UserPointsList(generics.ListAPIView):
	serializer_class = UserPointsSerializer
	permission_classes = [permissions.IsAuthenticated]
	def get_queryset(self):
		queryset = UserPoints.objects.all()
		tournament_id = self.kwargs.get('tournament_id')
		if tournament_id is not None:
			queryset = queryset.filter(tournament__id=int(tournament_id))
		return queryset

class UserPointsDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserPoints.objects.all()
    serializer_class = UserPointsSerializer

    def get_object(self):
	    username = self.kwargs.get('username')
	    tournament_id = self.kwargs.get('tournament_id')
	    user = get_object_or_404(User, username=username)
	    return get_object_or_404(UserPoints, user=user, tournament_id=tournament_id)

    def update(self, request, *args, **kwargs):
        username = kwargs.get('username')
        tournament_id = kwargs.get('tournamentId')
        user = get_object_or_404(User, username=username)
        instance = get_object_or_404(UserPoints, user=user, tournament_id=tournament_id)

        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.pop('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class UserPointsCreateView(generics.CreateAPIView):
    queryset = UserPoints.objects.all()
    serializer_class = UserPointsSerializer1

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
			
			




