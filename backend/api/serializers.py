from rest_framework import serializers 
from account.models import Account
from tournaments.models import Tournament
from tournaments.models import UserPoints
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
    Tournament_ID = serializers.CharField(source='tournament.id')
    class Meta:
        model = UserPoints
        fields = ['id', 'Tournament_ID', 'Username', 'deals', 'points']