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
from .serializers import ChangeUserPointsSerializer
from .serializers import PostUserPointsSerializer

class UserPointsList(generics.ListAPIView):
	serializer_class = UserPointsSerializer
	permission_classes = [permissions.IsAuthenticated]
	def get_queryset(self):
		queryset = UserPoints.objects.all()
		tournament_id = self.kwargs.get('tournament_id')
		if tournament_id is not None:
			queryset = queryset.filter(tournament__id=int(tournament_id))
		return queryset

class ChangeUserPointsView(generics.RetrieveUpdateAPIView):
    serializer_class = ChangeUserPointsSerializer

    def get_object(self):
        queryset = UserPoints.objects.all()
        user_id = self.kwargs.get('userId')
        tournament_id = self.kwargs.get('tournamentId')
        return queryset.filter(tournament__id=int(tournament_id), user__id=int(user_id)).first()

from rest_framework.views import APIView
from rest_framework.response import Response
class UserPointsCreateView(APIView):
    def post(self, request):
        user = User.objects.get(id=request.data['UserId'])
        tournament = Tournament.objects.get(id=request.data['TournamentId'])
        serializer = PostUserPointsSerializer(data={'user': request.data['UserId'], 'tournament': request.data['TournamentId'], 'deals': request.data['deals'],
                                               'points': request.data['points']})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

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
			return JsonResponse({'token':str(token), 'id': user.id}, status=201)
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
			return JsonResponse({'token':str(token), 'id': user.id}, status=201)

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
			
			




