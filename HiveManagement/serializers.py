from django.contrib.auth.models import User, Group
from rest_framework import serializers

#from models import WorkLog


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

# class WorkLogSerializer(serializers.HyperlinkedModelSerializer):
#     """
#     Serializing all the WorkLogs
#     """
#     class Meta:
#         model = WorkLog
#         field = ('field', 'task', 'teams', 'date_work', 'hives_alive')
