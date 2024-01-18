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
    class Meta:
        model = UserPoints
        fields = ['user', 'tournament', 'deals', 'points']

class UserPointsSerializer1(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    # Ensure that the tournament field is also correctly handled
    # depending on how you want it to be represented in the request
    tournament = serializers.PrimaryKeyRelatedField(queryset=Tournament.objects.all())

    class Meta:
        model = UserPoints
        fields = ['user', 'tournament', 'deals', 'points']