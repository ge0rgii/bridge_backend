from rest_framework import serializers 
from account.models import Account
from tournaments.models import Tournament
from tournaments.models import UserPoints
from django.contrib.auth.models import User
class AccountSerializer(serializers.ModelSerializer):
    Username = serializers.CharField(source='user.username')
    class Meta:
        model = Account
        fields = ['id', 'Username', 'avatar']
class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'name']

class UserPointsSerializer(serializers.ModelSerializer):
    Username = serializers.CharField(source='user.username')

    class Meta:
        model = UserPoints
        fields = ['id', 'Username', 'deals', 'points']

class ChangeUserPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoints
        fields = ['user', 'tournament', 'deals', 'points']
        read_only_fields = ['user', 'tournament']

class PostUserPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoints
        fields = ['user', 'tournament', 'deals', 'points']

